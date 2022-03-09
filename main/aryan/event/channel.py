"""事件通道实现"""
import asyncio
from typing import List, Type, Callable, Any, Optional
from loguru import logger
from functools import partial

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

    def filterIsInstance(self, event: Type[Event]): pass

    @staticmethod
    async def broadcast(event: Event):
        assert isinstance(event, AbstractEvent)
        event._intercepted = False
        asyncio.get_running_loop().create_task(callAndRemoveIfRequired(event))  # fixme

    async def nextEvent(self,
                        event: Type[Event],
                        timeout: float = 0,
                        priority: EventPriority = EventPriority.NORMAL,
                        filter: Optional[Callable[[Event], bool]] = None
                        ):
        """挂起当前协程 并等待从channel中获取指定类型的事件
        Args:
            event: 想要获取的事件类型
            priority: 事件优先级 见 [EventPriority]
            timeout: 目标超时
            filter: 临时的过滤器 将不会修改原channel
        """
        future = asyncio.get_running_loop().create_future()

        async def inside_listener(outer_future, ev: Event):
            outer_future.set_result(ev)
            print(ev)

        channel = self.filter(filter) if filter else self
        channel.subscribeOnce(event, partial(inside_listener, future), priority)

        if timeout:
            return await asyncio.wait_for(future, timeout)
        return await future

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
