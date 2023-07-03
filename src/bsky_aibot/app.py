import os
import time
import typing as t
from datetime import datetime, timedelta, timezone
import logging

import openai
from atproto import Client
from atproto.xrpc_client import models
from dateutil.parser import parse
from dotenv import load_dotenv

load_dotenv(verbose=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

HANDLE = os.getenv("HANDLE")
PASSWORD = os.getenv("PASSWORD")
openai.organization = os.environ.get("OPENAI_ORGANIZATION")
openai.api_key = os.environ.get("OPENAI_API_KEY")


class OpenAIMessage(t.TypedDict):
    role: str
    content: t.Optional[str]
    name: t.Optional[str]
    function_call: t.Optional[t.Dict]


def get_notifications(client: Client):
    response = client.bsky.notification.list_notifications()
    return response.notifications


def update_seen(client: Client, seenAt: datetime):
    response = client.bsky.notification.update_seen({"seenAt": seenAt.isoformat()})
    return


def filter_mentions_and_replies_from_notifications(ns: t.List["models.AppBskyNotificationListNotifications.Notification"]) -> t.List[models.AppBskyNotificationListNotifications.Notification]:
    return [n for n in ns if n.reason in ("mention", "reply")]


def filter_unread_notifications(ns: t.List["models.AppBskyNotificationListNotifications.Notification"], seen_at: datetime) -> t.List["models.AppBskyNotificationListNotifications.Notification"]:
    # IndexされてからNotificationで取得できるまでにラグがあるので、最後に見た時刻より少し前ににIndexされたものから取得する
    return [n for n in ns if seen_at - timedelta(minutes=2) < parse(n.indexedAt)]


def get_thread(client: Client, uri: str) -> "models.AppBskyFeedDefs.FeedViewPost":
    return client.bsky.feed.get_post_thread({"uri": uri})


# TODO: receive models.AppBskyFeedDefs.ThreadViewPost
def is_already_replied_to(feed_view: models.AppBskyFeedDefs.FeedViewPost, did: str) -> bool:
    replies = feed_view.thread.replies
    if replies is None:
        return False
    else:
        return any([reply.post.author.did == did for reply in replies])


def flatten_posts(thread: "models.AppBskyFeedDefs.ThreadViewPost") -> t.List[t.Dict[str, any]]:
    posts = [thread.post]

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


def reply_to(notification: models.AppBskyNotificationListNotifications.Notification) -> t.Union[models.AppBskyFeedPost.ReplyRef, models.AppBskyFeedDefs.ReplyRef]:
    parent = {
        "cid": notification.cid,
        "uri": notification.uri,
    }
    if notification.record.reply is None:
        return {"root": parent, "parent": parent}
    else:
        return {"root": notification.record.reply.root, "parent": parent}


def read_notifications_and_reply(client: Client, last_seen_at: datetime = None) -> datetime:
    logging.info(f"last_seen_at: {last_seen_at}")
    did = client.me.did

    seen_at = datetime.now(tz=timezone.utc)

    # unread countで判断するアプローチは、たまたまbsky.appで既読をつけてしまった場合に弱い
    ns = get_notifications(client)
    ns = filter_mentions_and_replies_from_notifications(ns)
    if last_seen_at is not None:
        ns = filter_unread_notifications(ns, last_seen_at)

    for notification in ns:
        thread = get_thread(client, notification.uri)
        if is_already_replied_to(thread, did):
            logging.info(f"Already replied to {notification.uri}")
            continue

        post_messages = thread_to_messages(thread, did)
        reply = generate_reply(post_messages)
        client.send_post(text=f"{reply}", reply_to=reply_to(notification))

    update_seen(client, seen_at)
    return seen_at


def main():
    client = Client()
    client.login(HANDLE, PASSWORD)
    seen_at = None
    while True:
        try:
            seen_at = read_notifications_and_reply(client, seen_at)
        except Exception as e:
            logging.exception(f"An error occurred: ${e}")
            time.sleep(300)
            client.login(HANDLE, PASSWORD)
        finally:
            time.sleep(10)


if __name__ == "__main__":
    main()
