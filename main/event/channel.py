"""事件通道实现"""
from typing import List, Type, Callable, Any, Coroutine

from . import Event, AbstractEvent
from .listener import (Listener, ListeningStatus, ConcurrencyKind, EventPriority, Handler, callAndRemoveIfRequired,
                       GlobalEventListeners, ListenerRegistry)


class EventChannel:
    _exceptionHandler: Callable

    def __init__(self, exception_handler: Callable=None):
        self._exceptionHandler = exception_handler

    def filter(self, filter: Callable[[Event], bool]):
        assert isinstance(filter, Callable)

    def exceptionHandler(self, handler: Callable[[Exception], None]):
        assert isinstance(handler, Callable)
        self._exceptionHandler = handler

    async def broadcast(self, event: Event):
        # TODO: classmethod or staticmethod
        assert isinstance(event, AbstractEvent)
        event._intercepted = False
        # TODO: 并发问题
        await callAndRemoveIfRequired(event)
        return event


    def registerListenerHost(self, listenerHost):
        pass

    def subscribe(self,
        event: Type[Event],
        handler: Callable[[Event], Any],
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.LOCKED
    ) -> Listener:
        # TODO: 何尝不直接获取参数的anno作为event type呢
        return self.subscribeInternal(event, self.createListener(handler, concurrencyKind, priority))

    def subscribeAlways(self,
        event: Type[Event],
        handler: Callable,
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.CONCURRENT
    ) -> Listener:
        async def wrapper(received_event):
            await handler(received_event)
            return ListeningStatus.LISTENING
        return self.subscribeInternal(event, self.createListener(wrapper, concurrencyKind, priority))


    def subscribeOnce(self,
        event: Type[Event],
        handler: Callable,
        priority: EventPriority=EventPriority.NORMAL
    ) -> Listener:
        async def wrapper(received_event):
            await handler(received_event)
            return ListeningStatus.STOPPED
        return self.subscribeInternal(event, self.createListener(wrapper, ConcurrencyKind.LOCKED, priority))

    # region impl

    def intercept(self, event: Event):
        pass
    def intercepted(self, event: Event):
        pass

    def subscribeInternal(self, eventClass: Type[Event], listener: Listener):
        GlobalEventListeners[listener.priority].append(ListenerRegistry(eventClass, listener))
        # TODO: 将handler与registry绑定 移除时销毁registry
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
