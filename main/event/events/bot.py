from .types import BotEvent, BotActiveEvent, BotPassiveEvent
from ...event import AbstractEvent


class BotOnlineEvent(BotActiveEvent, AbstractEvent):
    type = "BotOnlineEvent"
    qq: int

class BotOfflineEvent(BotEvent, AbstractEvent):
    pass

class BotOfflineEventActive(BotOfflineEvent, BotActiveEvent):
    type = "BotOfflineEventActive"
    qq: int

class BotOfflineEventForce(BotOfflineEvent, BotPassiveEvent):
    type = "BotOfflineEventForce"
    qq: int

class BotOfflineEventDropped(BotOfflineEvent, BotPassiveEvent):
    type = "BotOfflineEventDropped"
    qq: int

class BotReloginEvent(BotActiveEvent, AbstractEvent):
    type = "BotReloginEvent"
    qq: int
