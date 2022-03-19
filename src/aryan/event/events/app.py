from .. import AbstractEvent


class LaunchEvent(AbstractEvent):
    type: str = "LaunchEvent"


class ShutdownEvent(AbstractEvent):
    type: str = "ShutdownEvent"
