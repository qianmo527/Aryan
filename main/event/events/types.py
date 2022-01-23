from ...event import Event


class BotEvent(Event):
    """有关 [Bot] 的事件
    """

class BotPassiveEvent(BotEvent):
    """[Bot] 被动接收的事件
    """

class BotActiveEvent(BotEvent):
    """由 [Bot] 主动发起的动作的事件
    """

class GroupEvent(BotEvent):
    """有关群的事件
    """

class GroupOperableEvent(GroupEvent):
    """可由 [Member] 或 [Bot] 操作的事件
    """

class FriendEvent(BotEvent):
    """有关好友的事件
    """

class FriendInfoChangeEvent(FriendEvent):
    """有关好友信息更改的事件
    """

class StrangerEvent(BotEvent):
    """有关陌生人的事件
    """

class GroupMemberEvent(GroupEvent):
    """有关群成员的事件
    """

class GroupMemberInfoChangeEvent(GroupEvent):
    """有关群成员信息更改的事件
    """
    pass
