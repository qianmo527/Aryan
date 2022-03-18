"""事件通道实现"""
import asyncio
from asyncio import Event as asyncio_Event
import re
from typing import List, Type, Callable, Any, Optional, Dict, Union, Coroutine
from loguru import logger
from functools import partial

from . import Event, AbstractEvent
from .listener import (Listener, ListeningStatus, ConcurrencyKind, EventPriority, Handler, callAndRemoveIfRequired,
                       GlobalEventListeners, ListenerRegistry, ListenerHostInterface)
from ..message.data.single_message import SingleMessage
from ..utils import async_


class EventChannel:
    baseEventClass: Type[Event]

    def __init__(self, baseEventClass: Type[Event] = Event) -> None:
        self.baseEventClass = baseEventClass

    def filter(self, filter: Callable[[Event], bool]):
        assert isinstance(filter, Callable)
        parent: "EventChannel" = self
        channel = EventChannel(self.baseEventClass)

        def overriden_intercepted(func: Callable):
            async def listener_object(ev):
                filterResult: bool = False
                try:
                    filterResult = isinstance(ev, self.baseEventClass) and filter(ev)
                except Exception as e:
                    logger.warning(f"channel filter caught an exception: {e}")
                if filterResult:
                    return await func(ev)  # TODO
                else:
                    return ListeningStatus.LISTENING

            return parent.intercepted(listener_object)

        channel.intercepted = overriden_intercepted
        return channel

    def filterIsInstance(self, event: Type[Event]):
        return self.filter(lambda ev: isinstance(ev, event))

    @staticmethod
    async def broadcast(event: Event):
        assert isinstance(event, AbstractEvent)
        event._intercepted = False
        asyncio.get_running_loop().create_task(callAndRemoveIfRequired(event))

    async def nextEvent(self,
                        event: Type[Event],
                        timeout: float = None,
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

        channel = self.filter(filter) if filter else self
        channel.subscribeOnce(event, partial(inside_listener, future), priority)

        if timeout:
            return await asyncio.wait_for(future, timeout)
        return await future

    def registerListenerHost(self, listenerHost: Union[ListenerHostInterface, Type[ListenerHostInterface]]):
        pass

    def subscribe(self,
                  event: Type[Event],  # TODO
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
                      priority: EventPriority = EventPriority.NORMAL,
                      concurrencyKind: ConcurrencyKind = ConcurrencyKind.CONCURRENT
                      ) -> Listener:
        async def wrapper(received_event):
            asyncio.create_task(async_(handler(received_event)))
            return ListeningStatus.STOPPED

        return self.subscribeInternal(event, self.createListener(wrapper, concurrencyKind, priority))

    def subscribeMessages(self,
                          selector: Dict[str, Union[str, Callable, SingleMessage, List[SingleMessage]]],
                          default=False):
        # TODO 支持key自定义方法返回
        """订阅消息事件并自动回复

        Args:
            selector: dict形式的选择器, 其中key为触发的消息条件(可以正则), value为进行的操作(如[str], [SingleMessage], [List[SingleMessage]])
            default: 为True时, 将获取selector中的 `default` key作为默认回复, 如果default为空, 则获取selector最后一项的value作为默认回复

        Example:
            eventChannel.subscribeMessages({
                "hello": "hello!!",
                "签到.*?": Plain("签到成功"),
            }, default=True)
        """
        from .events.message import MessageEvent
        default_reply = selector.pop("default", list(selector.values())[-1])
        need_default = True
        async def func_call(value, ev):
            if isinstance(value, (str, SingleMessage, list)):
                return await ev.reply(value)
            elif isinstance(value, Coroutine):
                return await value(ev)
            elif isinstance(value, Callable):
                return value(ev)
        for k, v in selector.items():
            async def listener_obj(key, value, ev: MessageEvent):
                if re.match(key, ev.messageChain.contentToString()):
                    nonlocal need_default
                    need_default = False
                    return await func_call(value, ev)

            self.subscribe(MessageEvent, partial(listener_obj, k, v), concurrencyKind=ConcurrencyKind.CONCURRENT)
        self.subscribe(MessageEvent, lambda ev: func_call(default_reply, ev) if need_default else ...,
                       concurrencyKind=ConcurrencyKind.CONCURRENT)

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
