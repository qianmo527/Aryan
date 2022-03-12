from typing import Union

from .. import AbstractEvent
from .types import BotPassiveEvent, GroupEvent, FriendEvent, StrangerEvent
from ...contact.contact import Contact
from ...contact.friend import Friend
from ...message.data.chain import MessageChain
from ...contact.stranger import Stranger
from ...contact.member import Member


class MessageEvent(AbstractEvent, BotPassiveEvent):
    type: str
    sender: Contact
    messageChain: MessageChain

    def getSubject(self):
        return self.sender

    # TODO: 单Element或Element List支持
    async def reply(self, message: Union[MessageChain, str]):
        pass

    async def quoteReply(self, message: Union[MessageChain, str]):
        pass


class FriendMessage(MessageEvent, FriendEvent):
    type: str = "FriendMessage"
    sender: Friend
    messageChain: MessageChain

    async def reply(self, message: Union[MessageChain, str]):
        return await self.sender.bot.sendFriendMessage(self.sender, message)

    async def quoteReply(self, message: Union[MessageChain, str]):
        from ...message.data.source import Source
        return await self.sender.bot.sendFriendMessage(self.sender, message, self.messageChain.getFirst(Source))

class GroupMessage(MessageEvent, GroupEvent):
    type: str = "GroupMessage"
    sender: Member
    messageChain: MessageChain

    async def reply(self, message: Union[MessageChain, str]):
        return await self.sender.bot.sendGroupMessage(self.sender.group, message)

    async def quoteReply(self, message: Union[MessageChain, str]):
        from ...message.data.source import Source
        return await self.sender.bot.sendGroupMessage(self.sender.group, message, self.messageChain.getFirst(Source))

class TempMessage(MessageEvent, GroupEvent):
    type: str = "TempMessage"
    sender: Member
    messageChain: MessageChain

    async def reply(self, message: Union[MessageChain, str]):
        return await self.sender.bot.sendTempMessage(self.sender, message, group=self.sender.group)

    async def quoteReply(self, message: Union[MessageChain, str]):
        from ...message.data.source import Source
        return await self.sender.bot.sendTempMessage(self.sender, message, self.messageChain.getFirst(Source), self.sender.group)


class StrangerMessage(MessageEvent, StrangerEvent):
    type: str = "StrangerMessage"
    sender: Stranger
    messageChain: MessageChain
