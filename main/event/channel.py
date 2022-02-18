"""事件通道实现"""
from typing import TypeVar, Generic, List
from types import FunctionType

from . import Event
from .listener import Listener, ListeningStatus, ConcurrencyKind, EventPriority
from .filter import Filter


class EventChannel:
    _filter: Filter
    _exceptionHandler: FunctionType

    def __init__(self, filter: List[FunctionType]=[], exception_handler: FunctionType=None):
        self._filter = Filter(filter)
        self._exceptionHandler = exception_handler

    def filter(self, filter: FunctionType):
        assert isinstance(filter, FunctionType)
        _filter = self._filter + filter
        return EventChannel(filter=_filter.conditions)

    def exceptionHandler(self, handler: FunctionType):
        assert isinstance(handler, FunctionType)
        self._exceptionHandler = handler

    def broadcast(self, event: Event):
        pass

    def registerListenerHost(self, listenerHost):
        pass

    def subscribe(self,
        event: Event,
        handler: FunctionType,
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.LOCKED
    ) -> Listener:
        pass

    def subscribeAlways(self,
        event: Event,
        handler: FunctionType,
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.CONCURRENT
    ) -> Listener:
        pass

    def subscribeOnce(self,
        event: Event,
        handler: FunctionType,
        priority: EventPriority=EventPriority.NORMAL
    ):
        pass


class GlobalEventChannel(EventChannel):
    INSTANCE: "GlobalEventChannel" = None


GlobalEventChannel.INSTANCE = GlobalEventChannel()
