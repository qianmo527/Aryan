from pydantic import Field


from ...contact.member import MemberPerm
from ...contact.group import Group
from ...contact.member import Member

from ...event import AbstractEvent
from .types import (
    GroupEvent, GroupMemberEvent, GroupOperableEvent, GroupMemberInfoChangeEvent,
    BotPassiveEvent
)


class BotGroupPermissionChangeEvent(BotPassiveEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "BotGroupPermissionChangeEvent"
    origin: MemberPerm
    current: MemberPerm
    group: Group

class BotMuteEvent(BotPassiveEvent, GroupMemberInfoChangeEvent):
    type: str = "BotMuteEvent"
    duration_seconds: int = Field(..., alias="durationSeconds")
    operator: Member

class BotUnmuteEvent(BotPassiveEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "BotUnmuteEvent"
    operator: Member

class BotJoinGroupEvent(GroupEvent, BotPassiveEvent, AbstractEvent):
    type: str = "BotJoinGroupEvent"
    group: Group

class BotLeaveEvent(GroupMemberInfoChangeEvent, AbstractEvent):
    pass

class BotLeaveEventActive(BotLeaveEvent):
    type: str = "BotLeaveEventActive"
    group: Group

class BotLeaveEventKick(BotLeaveEvent):
    type: str = "BotLeaveEventKick"
    group: Group
    operator: Member

class GroupRecallEvent(GroupEvent, AbstractEvent):
    type: str = "GroupRecallEvent"
    authorId: int
    messageId: int
    time: int
    group: Group
    operator: Member = None

class GroupNameChangeEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "GroupNameChangeEvent"
    origin: str
    current: str
    group: Group
    operator: Member = None

class GroupEntranceAnnouncementChangeEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "GroupEntranceAnnouncementChangeEvent"
    origin: str
    current: str
    group: Group
    operator: Member = None

class GroupMuteAllEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "GroupMuteAllEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member = None

class GroupAllowAnonymousChatEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "GroupAllowAnonymousChatEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member = None

class GroupAllowConfessTalkEvent(AbstractEvent, GroupMemberInfoChangeEvent):
    type: str = "GroupAllowConfessTalkEvent"
    origin: bool
    new: bool
    group: Group
    is_by_bot: bool = Field(..., alias="isByBot")

class GroupAllowMemberInviteEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "GroupAllowMemberInviteEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member = None

class MemberJoinEvent(GroupMemberEvent, BotPassiveEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "MemberJoinEvent"
    member: Member
    invitor: Member = None

class MemberLeaveEvent(GroupMemberEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    pass

class MemberLeaveEventKick(MemberLeaveEvent, GroupOperableEvent):
    type: str = "MemberLeaveEventKick"
    member: Member
    operator: Member = None

class MemberLeaveEventQuit(MemberLeaveEvent):
    type: str = "MemberLeaveEventQuit"
    member: Member

class MemberCardChangeEvent(GroupMemberEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "MemberCardChangeEvent"
    origin: str
    current: str
    member: Member

class MemberSpecialTitleChangeEvent(GroupMemberEvent, GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "MemberSpecialTitleChangeEvent"
    origin: str
    current: str
    member: Member

class MemberPermissionChangeEvent(GroupMemberEvent, BotPassiveEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "MemberPermissionChangeEvent"
    origin: MemberPerm
    current: MemberPerm
    member: Member

class MemberMuteEvent(GroupMemberEvent, GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "MemberMuteEvent"
    duration_seconds: int = Field(..., alias="durationSeconds")
    member: Member
    operator: Member = None

class MemberUnmuteEvent(GroupMemberEvent, GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: str = "MemberUnmuteEvent"
    member: Member
    operator: Member = None

class MemberHonorChangeEvent(GroupMemberEvent, BotPassiveEvent, AbstractEvent):
    type: str = "MemberHonorChangeEvent"
    member: Member
    action: str  # Achieve / Lose
    honor: str
