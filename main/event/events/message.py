from .types import BotPassiveEvent, GroupEvent, FriendEvent, StrangerEvent
from ...contact.contact import Contact
from ...contact.friend import Friend
from ...message.data.chain import MessageChain
from ...contact.stranger import Stranger
from ...contact.member import Member


class MessageEvent(BotPassiveEvent):
    type: str
    sender: Contact
    messageChain: MessageChain

    def __repr__(self) -> str:
        return f"{self.__repr_name__}(sender={self.sender}, messageChain={self.messageChain})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(sender={self.sender}, messageChain={self.messageChain})"


class FriendMessage(MessageEvent, FriendEvent):
    type: str = "FriendMessage"
    sender: Friend
    messageChain: MessageChain

class GroupMessage(MessageEvent, GroupEvent):
    type: str = "GroupMessage"
    sender: Member
    messageChain: MessageChain

class TempMessage(MessageEvent, GroupEvent):
    type: str = "TempMessage"
    sender: Member
    messageChain: MessageChain


class StrangerMessage(MessageEvent, StrangerEvent):
    type: str = "StrangerMessage"
    sender: Stranger
    messageChain: MessageChain
