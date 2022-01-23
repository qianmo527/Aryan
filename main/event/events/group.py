from pydantic import Field

from ...event import AbstractEvent
from .types import (
    GroupEvent, GroupMemberEvent, GroupOperableEvent, GroupMemberInfoChangeEvent,
    BotPassiveEvent
)


class BotGroupPermissionChangeEvent(BotPassiveEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "BotGroupPermissionChangeEvent"
    orogin: MemberPerm
    current: MemberPerm
    group: Group

class BotMuteEvent(BotPassiveEvent, GroupMemberInfoChangeEvent):
    type = "BotMuteEvent"
    duration_seconds: int = Field(..., alias="durationSeconds")
    operator: Member

class BotUnmuteEvent(BotPassiveEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "BotUnmuteEvent"
    operator: Member

class BotJoinGroupEvent(GroupEvent, BotPassiveEvent, AbstractEvent):
    type = "BotJoinGroupEvent"
    group: Group

class BotLeaveEvent(GroupMemberInfoChangeEvent, AbstractEvent):
    pass

class BotLeaveEventActive(BotLeaveEvent):
    type = "BotLeaveEventActive"
    group: Group

class BotLeaveEventKick(BotLeaveEvent):
    type = "BotLeaveEventKick"
    group: Group
    operator: Member

class GroupRecallEvent(GroupEvent, AbstractEvent):
    type = "GroupRecallEvent"
    authorId: int
    messageId: int
    time: int
    group: Group
    operator: Member = None

class GroupNameChangeEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "GroupNameChangeEvent"
    origin: str
    current: str
    group: Group
    operator: Member = None

class GroupEntranceAnnouncementChangeEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "GroupEntranceAnnouncementChangeEvent"
    origin: str
    current: str
    group: Group
    operator: Member = None

class GroupMuteAllEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "GroupMuteAllEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member = None

class GroupAllowAnonymousChatEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type: "GroupAllowAnonymousChatEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member = None

class GroupAllowConfessTalkEvent(AbstractEvent, GroupMemberInfoChangeEvent):
    type = "GroupAllowConfessTalkEvent"
    origin: bool
    new: bool
    group: Group
    is_by_bot: bool = Field(..., alias="isByBot")

class GroupAllowMemberInviteEvent(GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "GroupAllowMemberInviteEvent"
    origin: bool
    current: bool
    group: Group
    operator: Member = None

class MemberJoinEvent(GroupMemberEvent, BotPassiveEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "MemberJoinEvent"
    member: Member
    invitor: Member = None

class MemberLeaveEvent(GroupMemberEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    pass

class MemberLeaveEventKick(MemberLeaveEvent, GroupOperableEvent):
    type = "MemberLeaveEventKick"
    member: Member
    operator: Member = None

class MemberLeaveEventQuit(MemberLeaveEvent):
    type = "MemberLeaveEventQuit"
    member: Member

class MemberCardChangeEvent(GroupMemberEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "MemberCardChangeEvent"
    origin: str
    current: str
    member: Member

class MemberSpecialTitleChangeEvent(GroupMemberEvent, GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "MemberSpecialTitleChangeEvent"
    origin: str
    current: str
    member: Member

class MemberPermissionChangeEvent(GroupMemberEvent, BotPassiveEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "MemberPermissionChangeEvent"
    origin: MemberPerm
    current: MemberPerm
    member: Member

class MemberMuteEvent(GroupMemberEvent, GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "MemberMuteEvent"
    duration_seconds: int = Field(..., alias="durationSeconds")
    member: Member
    operator: Member = None

class MemberUnmuteEvent(GroupMemberEvent, GroupOperableEvent, GroupMemberInfoChangeEvent, AbstractEvent):
    type = "MemberUnmuteEvent"
    member: Member
    operator: Member = None

class MemberHonorChangeEvent(GroupMemberEvent, BotPassiveEvent, AbstractEvent):
    type = "MemberHonorChangeEvent"
    member: Member
    action: str  # Achieve / Lose
    honor: str
