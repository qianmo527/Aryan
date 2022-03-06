"""事件通道实现"""
from typing import List, Type, Callable, Any
from loguru import logger

from . import Event, AbstractEvent
from .listener import (Listener, ListeningStatus, ConcurrencyKind, EventPriority, Handler, callAndRemoveIfRequired,
                       GlobalEventListeners, ListenerRegistry)


class EventChannel:

    def filter(self, filter: Callable[[Event], bool]):
        assert isinstance(filter, Callable)
        parent: "EventChannel" = self
        channel = EventChannel()

        def wrapper(func: Callable):
            async def listener_object(ev):
                filterResult: bool = False
                try:
                    baseEventClass = Event  # todo
                    filterResult = isinstance(ev, baseEventClass) and filter(ev)
                except Exception as e:
                    logger.warning(f"channel filter caught an exception: {e}")
                if filterResult:
                    return await func(ev)
                else:
                    return ListeningStatus.LISTENING
            return parent.intercepted(listener_object)

        channel.intercepted = wrapper
        return channel

    @staticmethod
    async def broadcast(event: Event):
        assert isinstance(event, AbstractEvent)
        event._intercepted = False
        await callAndRemoveIfRequired(event)
        return event

    def registerListenerHost(self, listenerHost):
        pass

    def subscribe(self,
                  event: Type[Event],
                  handler: Callable[[Event], Any],
                  priority: EventPriority = EventPriority.NORMAL,
                  concurrencyKind: ConcurrencyKind = ConcurrencyKind.LOCKED
                  ) -> Listener:
        # TODO: 何尝不直接获取参数的anno作为event type呢
        return self.subscribeInternal(event, self.createListener(handler, concurrencyKind, priority))

    def subscribeAlways(self,
                        event: Type[Event],
                        handler: Callable,
                        priority: EventPriority = EventPriority.NORMAL,
                        concurrencyKind: ConcurrencyKind = ConcurrencyKind.CONCURRENT
                        ) -> Listener:
        async def wrapper(received_event):
            await handler(received_event)
            return ListeningStatus.LISTENING

        return self.subscribeInternal(event, self.createListener(wrapper, concurrencyKind, priority))

    def subscribeOnce(self,
                      event: Type[Event],
                      handler: Callable,
                      priority: EventPriority = EventPriority.NORMAL
                      ) -> Listener:
        async def wrapper(received_event):
            await handler(received_event)
            return ListeningStatus.STOPPED

        return self.subscribeInternal(event, self.createListener(wrapper, ConcurrencyKind.LOCKED, priority))

    # region impl

    @staticmethod
    def intercepted(func: Callable):
        return func

    @staticmethod
    def subscribeInternal(eventClass: Type[Event], listener: Listener):
        GlobalEventListeners[listener.priority].append(ListenerRegistry(eventClass, listener))
        # TODO: 将handler与registry绑定 移除时销毁registry
        return listener

    def createListener(self, handler: Callable, concurrencyKind: ConcurrencyKind, priority: EventPriority):
        return Handler(
            handler=self.intercepted(handler),
            concurrencyKind=concurrencyKind,
            priority=priority
        )

    # endregion


class GlobalEventChannel(EventChannel):
    INSTANCE: "GlobalEventChannel" = None


GlobalEventChannel.INSTANCE = GlobalEventChannel()
