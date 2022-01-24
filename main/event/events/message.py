

from argparse import _CountAction
from types import MemberDescriptorType
from .types import BotPassiveEvent, GroupEvent, FriendEvent, StrangerEvent


class MessageEvent(BotPassiveEvent):
    sender: Contact
    messageChain: MessageChain

class FriendMessage(MessageEvent, FriendEvent):
    type = "FriendMessage"
    sender: Friend
    messageChain: MessageChain

class GroupMessage(MessageEvent, GroupEvent):
    type = "GroupMessage"
    sender: Member
    messageChain: MessageChain

class TempMessage(MessageEvent, GroupEvent):
    type = "TempMessage"
    sender: Member
    messageChain: MessageChain


class StrangerMessage(MessageEvent, StrangerEvent):
    type = "StrangerMessage"
    sender: Stranger
    messageChain: MessageChain
