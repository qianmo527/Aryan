from ...event import AbstractEvent
from .types import FriendEvent, FriendInfoChangeEvent
from pydantic import Field


class FriendInputStatusChangedEvent(FriendEvent, AbstractEvent):
    type = "FriendInputStatusChangeEvent"
    friend: Friend
    inputting: int

class FriendNickChangedEvent(AbstractEvent, FriendInfoChangeEvent):
    type = "FriendNickChangedEvent"
    friend: Friend
    from_name: str = Field(..., alias="from")
    to: str
