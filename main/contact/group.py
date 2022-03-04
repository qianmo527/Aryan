from typing import List, Union
from dataclasses import dataclass
from typing import TYPE_CHECKING


from .contact import Contact

from .member import Member
from .member import MemberPerm


@dataclass
class GroupSettings:
    entranceAnnouncement: str
    isMuteAll: bool
    isAllowedMemberInvite: bool
    isAutoApproveEnabled: bool
    isAnonymousChatEnabled: bool



class Group(Contact):
    id: int
    name: str
    settings: GroupSettings = None
    botMuteRemaining: int = 0
    permission: MemberPerm
    # owner: Member
    members: List[Member] = [] # TODO ContactList[NormalMember]
    announcements: str = None  # TODO
    isBotMuted: bool = not botMuteRemaining == 0  # TODO: refresh & set after initialization

    @property
    def avatarUrl(self) -> str:
        return f"https://p.qlogo.cn/gh/{id}/{id}/640"

    def __repr__(self) -> str:
        return f"Group({self.id}, name={self.name}, permission={self.permission})"

    def get(self, id: int):
        """获取群成员实例 不存在时返回 None

        当 id 为 Bot.id 时返回 botAsMember
        """
        return [i for i in self.members if i.id == id][0]

    def getOrFail(self, id: int):
        """获取群成员实例 不存在时抛出 NoSuchElementException

        当 id 为 Bot.id 时返回 botAsMember
        """
        pass

    def contains(self, id: int) -> bool:
        pass  # TODO Union[Friend, int] ... you know what to do.

    def quit(self) -> None:
        pass

    from ..message.data.message import Message
    from ..message.message_receipt import MessageReceipt
    def sendMessage(self, message: Union[Message, str]) -> MessageReceipt["Group"]:
        pass
    def setEssenceMessage(self, source):
        pass
