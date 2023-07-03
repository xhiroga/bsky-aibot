import pytest

from bsky_aibot.app import (filter_mentions_and_replies_from_notifications,
                            thread_to_messages)


class RecursiveDictWrapper:
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self.__dict__[key] = RecursiveDictWrapper(value)
            else:
                self.__dict__[key] = value

    def __getattr__(self, attr):
        if attr not in self.__dict__:
            return None
        return self.__dict__[attr]

    def __eq__(self, other):
        if isinstance(other, RecursiveDictWrapper):
            return self.__dict__ == other.__dict__
        return False


@pytest.mark.parametrize(
    "thread, expected",
    [
        ((None, "did:plc:d7mnkzaznaop33oiowcbco7g"), []),
        (
            (
                RecursiveDictWrapper(
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
                                        "parent": {
                                            "cid": "bafyreidhtcnigocyvgh5e4wbgfm6tisc5xujhna6yaimls73szdthh23my",
                                            "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhulhuys2r",
                                        },
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
                ),
                "did:plc:d7mnkzaznaop33oiowcbco7g",
            ),
            [
                {"role": "user", "content": "@aibot.bsky.social スイスのスーパーマーケットで旅行者が買うべき食べ物ってなんでしょうか？", "name": "hiroga_bsky_social"},
                {
                    "role": "assistant",
                    "content": "スイス旅行で試すべき食品はチーズとチョコレートがおすすめです。特にスイスはチーズフォンデュやラクレットで有名です。また、高品質なスイスチョコレートも見逃せません。その他、スイスのスーパーマーケットで見つけた新鮮な地元の生産物も試してみてください。",
                    "name": "aibot_bsky_social",
                },
            ],
        ),
        (
            (
                RecursiveDictWrapper(
                    {
                        "thread": {
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
                                        "root": {"cid": "bafyreidhtcnigocyvgh5e4wbgfm6tisc5xujhna6yaimls73szdthh23my", "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhulhuys2r"},
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
                            "parent": {
                                "$type": "app.bsky.feed.defs#threadViewPost",
                                "post": {
                                    "uri": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzjhxjagl72v",
                                    "cid": "bafyreiaygx42pwbxhll6qathsavbmwfqdlqbd47egemlvtqvoncw67qqmq",
                                    "author": {"did": "did:plc:d7mnkzaznaop33oiowcbco7g", "handle": "aibot.bsky.social", "viewer": {"muted": False, "blockedBy": False}, "labels": []},
                                    "record": {
                                        "text": "スイス旅行で試すべき食品はチーズとチョコレートがおすすめです。特にスイスはチーズフォンデュやラクレットで有名です。また、高品質なスイスチョコレートも見逃せません。その他、スイスのスーパーマーケットで見つけた新鮮な地元の生産物も試してみてください。",
                                        "$type": "app.bsky.feed.post",
                                        "reply": {
                                            "root": {
                                                "cid": "bafyreidhtcnigocyvgh5e4wbgfm6tisc5xujhna6yaimls73szdthh23my",
                                                "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhulhuys2r",
                                            },
                                            "parent": {
                                                "cid": "bafyreidhtcnigocyvgh5e4wbgfm6tisc5xujhna6yaimls73szdthh23my",
                                                "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzjhulhuys2r",
                                            },
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
                                "replies": [],
                            },
                            "replies": [],
                        }
                    }
                ),
                "did:plc:d7mnkzaznaop33oiowcbco7g",
            ),
            [
                {"role": "user", "content": "@aibot.bsky.social スイスのスーパーマーケットで旅行者が買うべき食べ物ってなんでしょうか？", "name": "hiroga_bsky_social"},
                {
                    "role": "assistant",
                    "content": "スイス旅行で試すべき食品はチーズとチョコレートがおすすめです。特にスイスはチーズフォンデュやラクレットで有名です。また、高品質なスイスチョコレートも見逃せません。その他、スイスのスーパーマーケットで見つけた新鮮な地元の生産物も試してみてください。",
                    "name": "aibot_bsky_social",
                },
                {"role": "user", "content": "いいですね〜！特にオススメの地元のブランドってありますか？", "name": "hiroga_bsky_social"},
            ],
        ),
    ],
)
def test_thread_to_messages(thread, expected):
    result = thread_to_messages(thread[0], thread[1])
    for a, b in zip(result, expected):
        assert a == b, f"{a} != {b}"



@pytest.mark.parametrize(
    "thread, expected",
    [
        ([], []),
        (
            [
                RecursiveDictWrapper({
                    "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzmbfyx47c2i",
                    "cid": "bafyreiakv74s2gej4bdaktsgcwkfgzqik7j2qq3zwdb335eqkao357koxe",
                    "author": {
                        "did": "did:plc:et47te5fb7uv64pbltu37lcc",
                        "handle": "hiroga.bsky.social",
                        "displayName": "さわら",
                        "avatar": "https://cdn.bsky.social/imgproxy/YzftAu-_2jnBJ8A0njUpxJBfu1t0ZAoW2sxl3243hVM/rs:fill:1000:1000:1:0/plain/bafkreie4yx4zpasdmvtzny7yndaygvzkf3d2yedzpvgoufuxomkrl7h5ee@jpeg",
                        "indexedAt": "2023-05-24T23:55:27.451Z",
                        "viewer": {
                            "muted": False,
                            "blockedBy": False,
                            "following": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.graph.follow/3jzkwyx3ado2g",
                            "followedBy": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.graph.follow/3jzi4toyt4l2y",
                        },
                        "labels": [],
                    },
                    "reason": "mention",
                    "record": {
                        "text": "ふと気になったんだけど、メールの特許って誰かが持ってるのでしょうか？ @aibot.bsky.social",
                        "$type": "app.bsky.feed.post",
                        "langs": [],
                        "facets": [
                            {
                                "$type": "app.bsky.richtext.facet",
                                "index": {"byteEnd": 121, "byteStart": 103},
                                "features": [{"did": "did:plc:d7mnkzaznaop33oiowcbco7g", "$type": "app.bsky.richtext.facet#mention"}],
                            }
                        ],
                        "createdAt": "2023-07-03T09:32:21.565Z",
                    },
                    "isRead": False,
                    "indexedAt": "2023-07-03T09:32:21.656Z",
                    "labels": [],
                }),
                RecursiveDictWrapper({
                    "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.like/3jzkvmuybrf2g",
                    "cid": "bafyreihrrxl6g66npsojzksml6lah6mjp5xbkkjt5mjn6jsuappus3gxpy",
                    "author": {
                        "did": "did:plc:et47te5fb7uv64pbltu37lcc",
                        "handle": "hiroga.bsky.social",
                        "displayName": "さわら",
                        "avatar": "https://cdn.bsky.social/imgproxy/YzftAu-_2jnBJ8A0njUpxJBfu1t0ZAoW2sxl3243hVM/rs:fill:1000:1000:1:0/plain/bafkreie4yx4zpasdmvtzny7yndaygvzkf3d2yedzpvgoufuxomkrl7h5ee@jpeg",
                        "indexedAt": "2023-05-24T23:55:27.451Z",
                        "viewer": {
                            "muted": False,
                            "blockedBy": False,
                            "following": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.graph.follow/3jzkwyx3ado2g",
                            "followedBy": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.graph.follow/3jzi4toyt4l2y",
                        },
                        "labels": [],
                    },
                    "reason": "like",
                    "reasonSubject": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzkvltqqkt23",
                    "record": {
                        "$type": "app.bsky.feed.like",
                        "subject": {"cid": "bafyreiblbmhpvxujy56qroiih3paqwego7ppbevgsaeutjm6xua5l5md6e", "uri": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzkvltqqkt23"},
                        "createdAt": "2023-07-02T20:28:47.448Z",
                    },
                    "isRead": True,
                    "indexedAt": "2023-07-02T20:28:47.742Z",
                    "labels": [],
                }),
                RecursiveDictWrapper({
                    "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzkv5uqagu2s",
                    "cid": "bafyreihplbu54am3qtbmzrphcpxd3oylo6omk56si2fitfyyyme7wu2bve",
                    "author": {
                        "did": "did:plc:et47te5fb7uv64pbltu37lcc",
                        "handle": "hiroga.bsky.social",
                        "displayName": "さわら",
                        "avatar": "https://cdn.bsky.social/imgproxy/YzftAu-_2jnBJ8A0njUpxJBfu1t0ZAoW2sxl3243hVM/rs:fill:1000:1000:1:0/plain/bafkreie4yx4zpasdmvtzny7yndaygvzkf3d2yedzpvgoufuxomkrl7h5ee@jpeg",
                        "indexedAt": "2023-05-24T23:55:27.451Z",
                        "viewer": {
                            "muted": False,
                            "blockedBy": False,
                            "following": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.graph.follow/3jzkwyx3ado2g",
                            "followedBy": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.graph.follow/3jzi4toyt4l2y",
                        },
                        "labels": [],
                    },
                    "reason": "reply",
                    "reasonSubject": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzkv2kmakh2k",
                    "record": {
                        "text": "もっと詳しく知りたいので、具体的な事例や類する事例、科学的な根拠などいただけませんか？",
                        "$type": "app.bsky.feed.post",
                        "langs": ["ja"],
                        "reply": {
                            "root": {"cid": "bafyreibcyrb2kzk225jyzz4m7qizc2vqsxaoqoqjvvvkacltv73o4tm26q", "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzkusvkvp72u"},
                            "parent": {"cid": "bafyreihhaywzcphtjj43mknbmv3czuhv4r6gps3hz6zcmqld5l5vs2ebyu", "uri": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzkv2kmakh2k"},
                        },
                        "createdAt": "2023-07-02T20:20:23.873Z",
                    },
                    "isRead": True,
                    "indexedAt": "2023-07-02T20:20:24.142Z",
                    "labels": [],
                }),
            ],
            [
                RecursiveDictWrapper({
                    "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzmbfyx47c2i",
                    "cid": "bafyreiakv74s2gej4bdaktsgcwkfgzqik7j2qq3zwdb335eqkao357koxe",
                    "author": {
                        "did": "did:plc:et47te5fb7uv64pbltu37lcc",
                        "handle": "hiroga.bsky.social",
                        "displayName": "さわら",
                        "avatar": "https://cdn.bsky.social/imgproxy/YzftAu-_2jnBJ8A0njUpxJBfu1t0ZAoW2sxl3243hVM/rs:fill:1000:1000:1:0/plain/bafkreie4yx4zpasdmvtzny7yndaygvzkf3d2yedzpvgoufuxomkrl7h5ee@jpeg",
                        "indexedAt": "2023-05-24T23:55:27.451Z",
                        "viewer": {
                            "muted": False,
                            "blockedBy": False,
                            "following": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.graph.follow/3jzkwyx3ado2g",
                            "followedBy": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.graph.follow/3jzi4toyt4l2y",
                        },
                        "labels": [],
                    },
                    "reason": "mention",
                    "record": {
                        "text": "ふと気になったんだけど、メールの特許って誰かが持ってるのでしょうか？ @aibot.bsky.social",
                        "$type": "app.bsky.feed.post",
                        "langs": [],
                        "facets": [
                            {
                                "$type": "app.bsky.richtext.facet",
                                "index": {"byteEnd": 121, "byteStart": 103},
                                "features": [{"did": "did:plc:d7mnkzaznaop33oiowcbco7g", "$type": "app.bsky.richtext.facet#mention"}],
                            }
                        ],
                        "createdAt": "2023-07-03T09:32:21.565Z",
                    },
                    "isRead": False,
                    "indexedAt": "2023-07-03T09:32:21.656Z",
                    "labels": [],
                }),
                RecursiveDictWrapper({
                    "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzkv5uqagu2s",
                    "cid": "bafyreihplbu54am3qtbmzrphcpxd3oylo6omk56si2fitfyyyme7wu2bve",
                    "author": {
                        "did": "did:plc:et47te5fb7uv64pbltu37lcc",
                        "handle": "hiroga.bsky.social",
                        "displayName": "さわら",
                        "avatar": "https://cdn.bsky.social/imgproxy/YzftAu-_2jnBJ8A0njUpxJBfu1t0ZAoW2sxl3243hVM/rs:fill:1000:1000:1:0/plain/bafkreie4yx4zpasdmvtzny7yndaygvzkf3d2yedzpvgoufuxomkrl7h5ee@jpeg",
                        "indexedAt": "2023-05-24T23:55:27.451Z",
                        "viewer": {
                            "muted": False,
                            "blockedBy": False,
                            "following": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.graph.follow/3jzkwyx3ado2g",
                            "followedBy": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.graph.follow/3jzi4toyt4l2y",
                        },
                        "labels": [],
                    },
                    "reason": "reply",
                    "reasonSubject": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzkv2kmakh2k",
                    "record": {
                        "text": "もっと詳しく知りたいので、具体的な事例や類する事例、科学的な根拠などいただけませんか？",
                        "$type": "app.bsky.feed.post",
                        "langs": ["ja"],
                        "reply": {
                            "root": {"cid": "bafyreibcyrb2kzk225jyzz4m7qizc2vqsxaoqoqjvvvkacltv73o4tm26q", "uri": "at://did:plc:et47te5fb7uv64pbltu37lcc/app.bsky.feed.post/3jzkusvkvp72u"},
                            "parent": {"cid": "bafyreihhaywzcphtjj43mknbmv3czuhv4r6gps3hz6zcmqld5l5vs2ebyu", "uri": "at://did:plc:d7mnkzaznaop33oiowcbco7g/app.bsky.feed.post/3jzkv2kmakh2k"},
                        },
                        "createdAt": "2023-07-02T20:20:23.873Z",
                    },
                    "isRead": True,
                    "indexedAt": "2023-07-02T20:20:24.142Z",
                    "labels": [],
                }),
            ],
        ),
    ],
)
def test_filter_mentions_and_replies_from_notifications(thread, expected):
    result = filter_mentions_and_replies_from_notifications(thread)
    for r, e in zip(result, expected):
        assert r == e, f"{r} != {e}"


if __name__ == "__main__":
    pytest.main()
