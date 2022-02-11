from enum import Enum
from pydantic import Field
from typing import TYPE_CHECKING
from datetime import datetime

from .user import User

if TYPE_CHECKING:
    from .friend import Friend
    from .group import Group


class MemberPerm(Enum):
    "描述群成员在群组中所具备的权限"

    Member = "MEMBER"  # 普通成员
    Administrator = "ADMINISTRATOR"  # 管理员
    Owner = "OWNER"  # 群主


class Member(User):
    id: int
    name: str = Field(..., alias="memberName")
    specialTitle: str
    permission: MemberPerm
    joinTimestamp: datetime
    lastSpeakTimestamp: datetime
    muteTimeRemaining: int
    group: "Group"

    def __repr__(self) -> str:
        return f"Member({self.id}, memberName={self.name}, specialTitle={self.specialTitle}, permission={self.permission} ,"\
        f"joinTimestamp={self.joinTimestamp}, lastSpeakTimestamp={self.lastSpeakTimestamp}, muteTimeRemaining={self.muteTimeRemaining} ,"\
        f"group={self.group})"

    def mute(self):
        pass

    from ..message.data.message import Message
    from ..message.message_receipt import MessageReceipt
    def sendMessage(self, message: Message) -> MessageReceipt["Member"]:
        pass
    def sendMessage(self, message: str) -> MessageReceipt["Member"]:
        pass

    def nudge(self):
        pass

    def asFriend(self) -> "Friend":
        try:
            return self.bot.getFriendOrFail(self.id)
        except:
            raise Exception(f"{self} is not a friend")
    def asFriendOrNone(self):
        return self.bot.getFriend(self.id)

    # TODO import
    def asStranger(self):
        try:
            return self.bot.getStrangerOrFail(id)
        except:
            raise Exception(f"{self} is not a stranger")

    def asStrangerOrNone(self):
        return self.bot.getStranger(id)

    @property
    def isFriend(self) -> bool:
        for i in self.bot.friends:
            if self.id == i.id:
                return True
    @property
    def isStranger(self) -> bool:
        for i in self.bot.strangers:
            if self.id == i.id:
                return True

    def nameCardOrNick(self):
        # TODO: Exception handling
        return self.nameCard or self.nickname
