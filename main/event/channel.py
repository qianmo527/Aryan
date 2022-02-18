"""事件通道实现"""
from typing import TypeVar, Generic
from types import FunctionType 

from . import Event
from .listener import Listener, ListeningStatus


class EventChannel:

    def filter(self, filter: FunctionType):  # TODO type checking
        return self


class GlobalEventChannel:
    INSTANCE: "GlobalEventChannel" = None

GlobalEventChannel.INSTANCE = GlobalEventChannel()

