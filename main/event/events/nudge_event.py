from typing import Dict
from pydantic import Field

from ...event import AbstractEvent
from .types import BotEvent


class NudgeEvent(BotEvent, AbstractEvent):
    type: str = "NudgeEvent"
    from_id: int = Field(..., alias="fromId")
    subject: Dict
    action: str
    suffix: str
    target: int
