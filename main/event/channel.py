"""事件通道实现"""
from typing import List, Type, Callable

from . import Event, AbstractEvent
from .listener import Listener, ListeningStatus, ConcurrencyKind, EventPriority, Handler, callAndRemoveIfRequired
from .filter import Filter


class EventChannel:
    _filter: Filter
    _exceptionHandler: Callable

    def __init__(self, filter: List[Callable]=[], exception_handler: Callable=None):
        self._filter = Filter(filter)
        self._exceptionHandler = exception_handler

    def filter(self, filter: Callable[[Event], bool]):
        assert isinstance(filter, Callable)
        _filter = self._filter + filter
        return EventChannel(filter=_filter.conditions)

    def exceptionHandler(self, handler: Callable[[Exception], ...]):
        assert isinstance(handler, Callable)
        self._exceptionHandler = handler

    def broadcast(self, event: Event):
        assert isinstance(event, AbstractEvent)
        event._intercepted = False
        # TODO: 并发问题
        callAndRemoveIfRequired(event)
        return event


    def registerListenerHost(self, listenerHost):
        pass

    def subscribe(self,
        event: Event,
        handler: Callable[..., ListeningStatus],
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.LOCKED
    ) -> Listener:
        pass

    def subscribeAlways(self,
        event: Event,
        handler: Callable[..., ...],
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.CONCURRENT
    ) -> Listener:
        pass

    def subscribeOnce(self,
        event: Event,
        handler: Callable[..., ...],
        priority: EventPriority=EventPriority.NORMAL
    ) -> Listener:
        pass

    # region impl

    def subscribeInternal(self, eventClass: Type[Event], listener: Listener):

        return listener

    @staticmethod
    def createListener(handler: Callable, concurrencyKind: ConcurrencyKind, priority: EventPriority):
        return Handler(
            handler = handler,
            concurrencyKind = concurrencyKind,
            priority = priority
        )

    # endregion


class GlobalEventChannel(EventChannel):
    INSTANCE: "GlobalEventChannel" = None


GlobalEventChannel.INSTANCE = GlobalEventChannel()
