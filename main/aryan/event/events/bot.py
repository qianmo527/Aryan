from .types import BotEvent, BotActiveEvent, BotPassiveEvent
from ...event import AbstractEvent


class BotOnlineEvent(BotActiveEvent, AbstractEvent):
    type: str = "BotOnlineEvent"
    qq: int

    def __repr_args__(self):
        return [(None, self.qq)]

class BotOfflineEvent(BotEvent, AbstractEvent):
    pass

class BotOfflineEventActive(BotOfflineEvent, BotActiveEvent):
    type: str = "BotOfflineEventActive"
    qq: int

class BotOfflineEventForce(BotOfflineEvent, BotPassiveEvent):
    type: str = "BotOfflineEventForce"
    qq: int

class BotOfflineEventDropped(BotOfflineEvent, BotPassiveEvent):
    type: str = "BotOfflineEventDropped"
    qq: int

class BotReloginEvent(BotActiveEvent, AbstractEvent):
    type: str = "BotReloginEvent"
    qq: int
