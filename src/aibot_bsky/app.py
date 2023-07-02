import os
import time
import typing as t
from datetime import datetime

import openai
from atproto import Client
from atproto.xrpc_client import models
from dotenv import load_dotenv

from atproto.xrpc_client.models import ids

load_dotenv(verbose=True)

HANDLE = os.getenv("HANDLE")
PASSWORD = os.getenv("PASSWORD")

LAST_REPLIED_DATETIME_FILE = "./last_replied_datetime.txt"

openai.organization = os.environ.get("OPENAI_ORGANIZATION")
openai.api_key = os.environ.get("OPENAI_API_KEY")


class OpenAIMessage(t.TypedDict):
    # <https://platform.openai.com/docs/api-reference/chat/create
    role: str
    content: t.Optional[str]
    name: t.Optional[str]
    function_call: t.Optional[t.Dict]


def now():
    return datetime.now().isoformat()


def get_followers(client: Client, handle: str):
    # <https://atproto.com/lexicons/app-bsky-graph#appbskygraphgetfollowers>
    # TODO: cursor
    response = client.bsky.graph.get_followers({"actor": handle})
    return response.followers


def get_follows(client: Client, handle: str):
    # <https://atproto.com/lexicons/app-bsky-graph#appbskygraphgetfollows
    # TODO: cursor
    response = client.bsky.graph.get_follows({"actor": handle})
    return response.follows


def follow(client: Client, did: str, subject: str):
    response = client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(
                repo=did,
                collection=ids.AppBskyGraphFollow,
                record=models.AppBskyGraphFollow.Main(
                    createdAt=now(),
                    subject=subject,
                ),
            ))
    print(response)


def follow_back(
    client: Client,
    did: str,
    followers: t.List["models.AppBskyActorDefs.ProfileView"],
    follows: t.List["models.AppBskyActorDefs.ProfileView"],
):
    not_followed_yet = [follower for follower in followers if follower.did not in [follow.did for follow in follows]]
    for follower in not_followed_yet:
        follow(client, did, follower.did)


def get_last_replied_datetime() -> str:
    if os.path.exists(LAST_REPLIED_DATETIME_FILE):
        with open(LAST_REPLIED_DATETIME_FILE, "r") as f:
            return f.read().strip()
    else:
        return None


def update_last_replied_datetime(datetime_iso8601: str):
    with open(LAST_REPLIED_DATETIME_FILE, "w") as f:
        f.write(datetime_iso8601)


def get_timeline(client: Client) -> "models.AppBskyFeedGetTimeline.Response":
    # TODO: cursor
    return client.bsky.feed.get_timeline({"algorithm": "reverse-chronological"})


def is_seen(post: models.AppBskyFeedDefs.PostView, last_replied_datetime: t.Union[str, None]) -> bool:
    if last_replied_datetime is None:
        return False
    else:
        seen = post.record.createdAt > last_replied_datetime
        return seen


def filter_and_sort_timeline(feed: t.List["models.AppBskyFeedDefs.FeedViewPost"], last_replied_datetime: t.Union[str, None]) -> t.List["models.AppBskyFeedDefs.FeedViewPost"]:
    # keep only unseen posts and sort by createdAt asc
    filtered_feed = [feed_view for feed_view in feed if is_seen(feed_view.post, last_replied_datetime)]
    sorted_feed = sorted(filtered_feed, key=lambda feed_view: feed_view.post.record.createdAt)
    return sorted_feed


def is_mention(feature: t.Dict[str, str], did: str) -> bool:
    return feature["_type"] == "app.bsky.richtext.facet#mention" and feature["did"] == did


def does_post_have_mention(post: models.AppBskyFeedDefs.PostView, did: str) -> bool:
    facets = post.record.facets
    if facets is None:
        return False
    else:
        return any([any([is_mention(feature, did) for feature in facet.features]) for facet in facets])


def is_reply_to_me(feed_view: models.AppBskyFeedDefs.FeedViewPost, did: str) -> bool:
    reply = feed_view.reply
    if reply is None:
        return False
    else:
        if reply.parent.author.did == did:
            return True
        else:
            return False


def get_thread(client: Client, uri: str) -> "models.AppBskyFeedDefs.FeedViewPost":
    return client.bsky.feed.get_post_thread({"uri": uri})


def flatten_posts(thread: "models.AppBskyFeedDefs.ThreadViewPost") -> t.List[t.Dict[str, any]]:
    posts = [thread.post]

    # recursive case: if there is a parent, extend the list with posts from the parent
    parent = thread.parent
    if parent is not None:
        posts.extend(flatten_posts(parent))

    return posts


def get_oepnai_chat_message_name(name: str) -> str:
    # should be '^[a-zA-Z0-9_-]{1,64}$'
    return name.replace(".", "_")


def posts_to_sorted_messages(posts: t.List[models.AppBskyFeedDefs.PostView], assistant_did: str) -> t.List[OpenAIMessage]:
    sorted_posts = sorted(posts, key=lambda post: post.indexedAt)
    messages = []
    for post in sorted_posts:
        role = "assistant" if post.author.did == assistant_did else "user"
        messages.append(OpenAIMessage(role=role, content=post.record.text, name=get_oepnai_chat_message_name(post.author.handle)))
        messages.append(OpenAIMessage(role="user", content=post.record.text, name=get_oepnai_chat_message_name(post.author.handle)))
    return messages


def thread_to_messages(thread: "models.AppBskyFeedGetPostThread.Response", did: str) -> t.List[OpenAIMessage]:
    if thread is None:
        return []
    posts = flatten_posts(thread.thread)
    messages = posts_to_sorted_messages(posts, did)
    return messages


def generate_reply(post_messages: t.List[OpenAIMessage]):
    # <https://platform.openai.com/docs/api-reference/chat/create>
    messages = [{"role": "system", "content": "Reply friendly in 280 characters or less. No @mentions."}]
    messages.extend(post_messages)
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    first = chat_completion.choices[0]
    return first.message.content


def reply_to(post):
    parent = {
        "cid": post.cid,
        "uri": post.uri,
    }
    if post.record.reply is None:
        return {"root": parent, "parent": parent}
    else:
        return {"root": post.record.reply.root, "parent": parent}


def main():
    client = Client()
    profile = client.login(HANDLE, PASSWORD)

    bot_followers = get_followers(client, HANDLE)
    bot_follows = get_follows(client, HANDLE)
    follow_back(client, profile.did, bot_followers, bot_follows)

    timeline = get_timeline(client)
    # should check with latest reply, not last replied datetime
    last_replied_datetime = get_last_replied_datetime()
    new_feed = filter_and_sort_timeline(timeline.feed, last_replied_datetime)

    for feed_view in new_feed:
        mentioned = does_post_have_mention(feed_view.post, profile.did)
        reply_to_me = is_reply_to_me(feed_view, profile.did)
        if mentioned or reply_to_me:
            if reply_to_me:
                thread = get_thread(client, feed_view.post.uri)
                post_messages = thread_to_messages(thread, profile.did)
            else:
                post_messages = posts_to_sorted_messages([feed_view.post], profile.did)
            reply = generate_reply(post_messages)
            client.send_post(text=f"{reply}", reply_to=reply_to(feed_view.post))
            update_last_replied_datetime(feed_view.post.record.createdAt)


if __name__ == "__main__":
    # TODO: Keep token.
    while True:
        main()
        print("Sleeping for 30 seconds...")
        time.sleep(30)
