import os
import typing as t
from datetime import datetime
import openai
from atproto import Client
from atproto.xrpc_client import models
from dotenv import load_dotenv

load_dotenv(verbose=True)

HANDLE = os.getenv("HANDLE")
PASSWORD = os.getenv("PASSWORD")

LAST_REPLIED_DATETIME_FILE = "./last_replied_datetime.txt"

openai.organization = os.environ.get("OPENAI_ORGANIZATION")
openai.api_key = os.environ.get("OPENAI_API_KEY")


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


def follow(client: Client, subject: str):
    # <https://atproto.com/lexicons/app-bsky-graph#appbskygraphfollow>
    data_model = {
        "subject": subject,
        "createdAt": now(),
    }
    response = client.bsky._client.invoke_procedure(
        "app.bsky.graph.follow", data=data_model, input_encoding="application/json"
    )
    print(response)


def follow_back(
    client: Client,
    followers: t.List["models.AppBskyActorDefs.ProfileView"],
    follows: t.List["models.AppBskyActorDefs.ProfileView"],
):
    not_followed_yet = [
        follower
        for follower in followers
        if follower.did not in [follow.did for follow in follows]
    ]
    for follower in not_followed_yet:
        follow(client, follower.did)


def get_last_replied_datetime() -> str:
    if os.path.exists(LAST_REPLIED_DATETIME_FILE):
        with open(LAST_REPLIED_DATETIME_FILE, 'r') as f:
            return f.read().strip()
    else:
        return None


def update_last_replied_datetime(datetime_iso8601: str):
    with open(LAST_REPLIED_DATETIME_FILE, 'w') as f:
        f.write(datetime_iso8601)


def get_timeline(client: Client) -> 'models.AppBskyFeedGetTimeline.Response':
    # TODO: cursor
    return client.bsky.feed.get_timeline({"algorithm": "reverse-chronological"})


def is_seen(post: models.AppBskyFeedDefs.PostView, last_replied_datetime: t.Union[str, None]) -> bool:
    if last_replied_datetime is None:
        return False
    else:
        seen = post.record.createdAt > last_replied_datetime
        return seen


def filter_and_sort_timeline(feed: t.List['models.AppBskyFeedDefs.FeedViewPost'], last_replied_datetime: t.Union[str, None]) -> t.List['models.AppBskyFeedDefs.FeedViewPost']:
    # keep only unseen posts and sort by createdAt asc
    filtered_feed = [feed_view for feed_view in feed if is_seen(feed_view.post, last_replied_datetime)]
    sorted_feed = sorted(filtered_feed, key=lambda feed_view: feed_view.post.record.createdAt)
    return sorted_feed


def is_mention(feature: t.Dict[str, str], did: str) -> bool:
    return (
        feature["_type"] == "app.bsky.richtext.facet#mention" and feature["did"] == did
    )


def does_post_have_mention(post: models.AppBskyFeedDefs.FeedViewPost, did: str) -> bool:
    facets = post.record.facets
    if facets is None:
        return False
    else:
        return any(
            [
                any([is_mention(feature, did) for feature in facet.features])
                for facet in facets
            ]
        )


def generate_reply(text):
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4", messages=[
            {"role": "system", "content": 'Reply in 280 characters or less. No @mentions.'},
            {"role": "user", "content": text}
        ]
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

    follow_back(client, bot_followers, bot_follows)

    timeline = get_timeline(client)
    last_replied_datetime = get_last_replied_datetime()
    new_feed = filter_and_sort_timeline(timeline.feed, last_replied_datetime)

    for feed_view in new_feed:
        mentioned = does_post_have_mention(feed_view.post, profile.did)
        if mentioned:
            # TODO: Thread
            reply = generate_reply(feed_view.post.record.text)
            client.send_post(text=f"{reply}", reply_to=reply_to(feed_view.post))
            update_last_replied_datetime(feed_view.post.record.createdAt)


if __name__ == "__main__":
    # TODO: loop main() with 30 seconds interval
    main()
