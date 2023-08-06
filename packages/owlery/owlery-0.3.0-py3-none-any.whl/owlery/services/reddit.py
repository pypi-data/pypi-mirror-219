import datetime as dt
import typing as t

from dataclasses import dataclass

import praw

from . import Message, Service


@dataclass
class Redditor:
    id: str
    name: str


@dataclass
class RedditMessage(Message):
    author: t.Optional[t.Union[praw.reddit.Redditor, Redditor]] = None
    body: t.Optional[str] = None


class Reddit(Service):
    name = "reddit"

    can_receive = True
    can_send = True

    def __init__(
        self,
        client_id,
        client_secret,
        username,
        password,
        user_agent,
        **kwargs,
    ):
        user_agent = f"{user_agent} (by u/{username})"

        self.api = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent,
        )

        super().__init__(**kwargs)

    def receive(self, limit=100, **kwargs):
        for message in self.api.inbox.unread(limit=limit):
            yield RedditMessage(
                author=message.author,
                body=message.body,
                date=dt.datetime.fromtimestamp(message.created_utc),
                id=message.id,
            )

            message.mark_read()

    def send(
        self,
        author: t.Union[praw.reddit.Redditor, Redditor, str],
        body: str,
        **kwargs,
    ):
        pass
