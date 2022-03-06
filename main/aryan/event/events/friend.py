from ...event import AbstractEvent
from .types import FriendEvent, FriendInfoChangeEvent
from pydantic import Field

from ...contact.friend import Friend


class FriendInputStatusChangedEvent(FriendEvent, AbstractEvent):
    type: str = "FriendInputStatusChangeEvent"
    friend: Friend
    inputting: bool

    def __repr__(self) -> str:
        return f"FriendInputStatusChangedEvent(friend={self.friend}, inputting={self.inputting})"

    def __str__(self) -> str:
        return f"FriendInputStatusChangedEvent(friend={self.friend}, inputting={self.inputting})"

class FriendNickChangedEvent(AbstractEvent, FriendInfoChangeEvent):
    type: str = "FriendNickChangedEvent"
    friend: Friend
    from_name: str = Field(..., alias="from")
    to: str
