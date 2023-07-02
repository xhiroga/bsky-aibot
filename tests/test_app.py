import pytest

from aibot_bsky.app import thread_to_messages


@pytest.mark.parametrize(
    "thread, expected",
    [
        ([], []),
        (
            [
                {
                    "thread": {
                        "$type": "app.bsky.feed.defs#threadViewPost",
                        "post": {
                            "uri": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzjhxjagl72v",
                            "cid": "bafyreiaygx42pwbxhll6qathsavbmwfqdlqbd47egemlvtqvoncw67qqmq",
                            "author": {"did": "did:plc:d7mnkzaznaop33oiowcbco7g", "handle": "aibot.bsky.social", "viewer": {"muted": False, "blockedBy": False}, "labels": []},
                            "record": {
                                "text": "スイス旅行で試すべき食品はチーズとチョコレートがおすすめです。特にスイスはチーズフォンデュやラクレットで有名です。また、高品質なスイスチョコレートも見逃せません。その他、スイスのスーパーマーケットで見つけた新鮮な地元の生産物も試してみてください。",
                                "$type": "app.bsky.feed.post",
                                "reply": {
                                    "root": {"cid": "bafyreidhtcnigocyvgh5e4wbgfm6tisc5xujhna6yaimls73szdthh23my", "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhulhuys2r"},
                                    "parent": {"cid": "bafyreidhtcnigocyvgh5e4wbgfm6tisc5xujhna6yaimls73szdthh23my", "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhulhuys2r"},
                                },
                                "createdAt": "2023-07-02T15:51:31.629127",
                            },
                            "replyCount": 1,
                            "repostCount": 0,
                            "likeCount": 0,
                            "indexedAt": "2023-07-02T06:51:32.383Z",
                            "viewer": {},
                            "labels": [],
                        },
                        "parent": {
                            "$type": "app.bsky.feed.defs#threadViewPost",
                            "post": {
                                "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhulhuys2r",
                                "cid": "bafyreidhtcnigocyvgh5e4wbgfm6tisc5xujhna6yaimls73szdthh23my",
                                "author": {
                                    "did": "did:plc:et47te5fb7uv64pbltu37lcc",
                                    "handle": "hiroga.bsky.social",
                                    "displayName": "さわら",
                                    "avatar": "https://cdn.bsky.social/imgproxy/YzftAu-_2jnBJ8A0njUpxJBfu1t0ZAoW2sxl3243hVM/rs:fill:1000:1000:1:0/plain/bafkreie4yx4zpasdmvtzny7yndaygvzkf3d2yedzpvgoufuxomkrl7h5ee@jpeg",
                                    "viewer": {
                                        "muted": False,
                                        "blockedBy": False,
                                        "following": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.graph.follow/3jzi4jqfh632f",
                                        "followedBy": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.graph.follow/3jzi4toyt4l2y",
                                    },
                                    "labels": [],
                                },
                                "record": {
                                    "text": "@aibot.bsky.social スイスのスーパーマーケットで旅行者が買うべき食べ物ってなんでしょうか？",
                                    "$type": "app.bsky.feed.post",
                                    "langs": ["ja"],
                                    "facets": [
                                        {
                                            "$type": "app.bsky.richtext.facet",
                                            "index": {"byteEnd": 18, "byteStart": 0},
                                            "features": [{"did": "did:plc:d7mnkzaznaop33oiowcbco7g", "$type": "app.bsky.richtext.facet#mention"}],
                                        }
                                    ],
                                    "createdAt": "2023-07-02T06:49:53.771Z",
                                },
                                "replyCount": 1,
                                "repostCount": 0,
                                "likeCount": 0,
                                "indexedAt": "2023-07-02T06:49:54.079Z",
                                "viewer": {},
                                "labels": [],
                            },
                            "replies": [],
                        },
                        "replies": [
                            {
                                "$type": "app.bsky.feed.defs#threadViewPost",
                                "post": {
                                    "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhzotcdp2v",
                                    "cid": "bafyreieilzzs3vhdtllqvojvxlurnnnxbk2aku2ds6lvg5lgzogjdi2tv4",
                                    "author": {
                                        "did": "did:plc:et47te5fb7uv64pbltu37lcc",
                                        "handle": "hiroga.bsky.social",
                                        "displayName": "さわら",
                                        "avatar": "https://cdn.bsky.social/imgproxy/YzftAu-_2jnBJ8A0njUpxJBfu1t0ZAoW2sxl3243hVM/rs:fill:1000:1000:1:0/plain/bafkreie4yx4zpasdmvtzny7yndaygvzkf3d2yedzpvgoufuxomkrl7h5ee@jpeg",
                                        "viewer": {
                                            "muted": False,
                                            "blockedBy": False,
                                            "following": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.graph.follow/3jzi4jqfh632f",
                                            "followedBy": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.graph.follow/3jzi4toyt4l2y",
                                        },
                                        "labels": [],
                                    },
                                    "record": {
                                        "text": "いいですね〜！特にオススメの地元のブランドってありますか？",
                                        "$type": "app.bsky.feed.post",
                                        "langs": ["ja"],
                                        "reply": {
                                            "root": {
                                                "cid": "bafyreidhtcnigocyvgh5e4wbgfm6tisc5xujhna6yaimls73szdthh23my",
                                                "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhulhuys2r",
                                            },
                                            "parent": {
                                                "cid": "bafyreiaygx42pwbxhll6qathsavbmwfqdlqbd47egemlvtqvoncw67qqmq",
                                                "uri": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzjhxjagl72v",
                                            },
                                        },
                                        "createdAt": "2023-07-02T06:52:45.065Z",
                                    },
                                    "replyCount": 0,
                                    "repostCount": 0,
                                    "likeCount": 0,
                                    "indexedAt": "2023-07-02T06:52:45.355Z",
                                    "viewer": {},
                                    "labels": [],
                                },
                                "replies": [],
                            }
                        ],
                    }
                }
            ],
            [
                {"role": "user", "content": "@aibot.bsky.social スイスのスーパーマーケットで旅行者が買うべき食べ物ってなんでしょうか？", "name": "さわら"},
                {"role": "assistant", "content": "スイス旅行で試すべき食品はチーズとチョコレートがおすすめです。特にスイスはチーズフォンデュやラクレットで有名です。また、高品質なスイスチョコレートも見逃せません。その他、スイスのスーパーマーケットで見つけた新鮮な地元の生産物も試してみてください。", "name": "aibot"},
                {"role": "user", "content": "いいですね〜！特にオススメの地元のブランドってありますか？", "name": "さわら"}
            ],
        ),
    ],
)
def test_thread_to_messages(thread, expected):
    result = thread_to_messages(thread)
    assert result == expected
