"""事件通道实现"""
import asyncio
from asyncio import Lock
import re
from typing import Iterable, List, Type, Callable, Any, Optional, Dict, Union, Coroutine
from loguru import logger
from functools import partial, wraps
import inspect

from . import Event, AbstractEvent
from .listener import (Listener, ListeningStatus, ConcurrencyKind, EventPriority, Handler, callAndRemoveIfRequired,
                       GlobalEventListeners, ListenerRegistry, ListenerHostInterface)
from ..message.data.single_message import SingleMessage
from ..utils import async_, get_event_from_func


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
                    return await async_(func(ev))
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
        if isinstance(listenerHost, type):
            listenerHost = listenerHost()

        for func in [i[1] for i in inspect.getmembers(listenerHost, lambda value: getattr(value, "__handler__", None))]:
            self.subscribe(handler=func, concurrencyKind=ConcurrencyKind.CONCURRENT)

    def subscribe(self,
                  event: Type[Event]=None,
                  handler: Callable[[Event], Any]=lambda ev: print("received event:", ev.__class__.__name__),
                  priority: EventPriority = EventPriority.NORMAL,
                  concurrencyKind: ConcurrencyKind = ConcurrencyKind.LOCKED
                  ) -> Listener:
        if event is None:
            event = get_event_from_func(handler)

        if return_value := handler.__annotations__.get("return"):
            if return_value is ListeningStatus.LISTENING:
                if isinstance(event, Iterable):
                    return [self.subscribeAlways(ev, handler, priority, concurrencyKind) for ev in event]
                return self.subscribeAlways(event, handler, priority, concurrencyKind)
            elif return_value is ListeningStatus.STOPPED:
                if isinstance(event, Iterable):
                    return [self.subscribeOnce(ev, handler, priority, concurrencyKind) for ev in event]
                return self.subscribeOnce(event, handler, priority, concurrencyKind)

        return self.subscribeInternal(event or self.baseEventClass, self.createListener(handler, concurrencyKind, priority))

    def subscribeAlways(self,
                        event: Type[Event]=None,
                        handler: Callable=lambda ev: print("received event:", ev.__class__.__name__),
                        priority: EventPriority = EventPriority.NORMAL,
                        concurrencyKind: ConcurrencyKind = ConcurrencyKind.CONCURRENT
                        ) -> Listener:
        async def wrapper(received_event):
            await async_(handler(received_event))
            return ListeningStatus.LISTENING

        if event is None:
            event = get_event_from_func(handler)
        return self.subscribeInternal(event or self.baseEventClass, self.createListener(wrapper, concurrencyKind, priority))

    def subscribeOnce(self,
                      event: Type[Event]=None,
                      handler: Callable=lambda ev: print("received event:", ev.__class__.__name__),
                      priority: EventPriority = EventPriority.NORMAL,
                      concurrencyKind: ConcurrencyKind = ConcurrencyKind.CONCURRENT
                      ) -> Listener:
        async def wrapper(received_event):
            asyncio.create_task(async_(handler(received_event)))
            return ListeningStatus.STOPPED

        if event is None:
            event = get_event_from_func(handler)
        return self.subscribeInternal(event or self.baseEventClass, self.createListener(wrapper, concurrencyKind, priority))

    def trigger(self,
        event: Event=None,
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.LOCKED):
        """subscribe的装饰器版本
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.subscribe(event, func, priority, concurrencyKind)
            return wrapper
        return decorator

    def triggerAlways(self,
        event: Event=None,
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.CONCURRENT):
        """subscribeAlways的装饰器版本
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.subscribeAlways(event, func, priority, concurrencyKind)
            return wrapper
        return decorator

    def triggerOnce(self,
        event: Event=None,
        priority: EventPriority=EventPriority.NORMAL,
        concurrencyKind: ConcurrencyKind=ConcurrencyKind.CONCURRENT):
        """subscribeOnce的装饰器版本
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            self.subscribeOnce(event, func, priority, concurrencyKind)
            return wrapper
        return decorator

    def subscribeMessages(self,
                          selector: Dict[str, Union[str, Callable, SingleMessage, List[SingleMessage]]],
                          default=False):
        # TODO 支持key自定义方法返回
        """订阅消息事件并自动回复

        Args:
            selector: dict形式的选择器, 其中key为触发的消息条件, value为进行的操作(如[str], [SingleMessage], [List[SingleMessage]], [Callable])
            default: 为True时, 将获取selector中的 `default` key作为默认回复, 如果default为空, 则获取selector最后一项的value作为默认回复

        Example:
            eventChannel.subscribeMessages({
                "hello": "hello!!",
                "签到": Plain("签到成功"),
                "default": "default reply"
            }, default=True)
        """
        from .events.message import MessageEvent
        default_reply = selector.pop("default", list(selector.values())[-1])
        async def func_call(value, ev):
            if isinstance(value, (str, SingleMessage, list)):
                return await ev.reply(value)
            elif isinstance(value, Callable):
                return await async_(value(ev))

        lock = Lock()
        can_reply = True
        for k, v in selector.items():
            async def listener_obj(key, value, ev: MessageEvent):
                if ev.messageChain.contentToString() == key:
                    nonlocal lock, can_reply
                    async with lock:
                        can_reply = False
                        return await func_call(value, ev)

            self.subscribe(MessageEvent, partial(listener_obj, k, v), concurrencyKind=ConcurrencyKind.CONCURRENT)
        if default:
            async def default_wrapper(ev):
                nonlocal lock, default_reply, can_reply
                async with lock:
                    if can_reply:
                        return await func_call(default_reply, ev)
                    can_reply = True
            self.subscribe(MessageEvent, default_wrapper, concurrencyKind=ConcurrencyKind.CONCURRENT)

    @staticmethod
    def addBackgroundTask(func: Optional[Union[Coroutine, Callable]]=None):
        if func is None:
            def wrapper(func_):
                EventChannel.addBackgroundTask(func_)
                return func_
            return wrapper

        async def listener(ev):
            asyncio.create_task(func())
        from .events.app import LaunchEvent
        GlobalEventChannel.INSTANCE.subscribe(LaunchEvent, listener, EventPriority.HIGHEST, ConcurrencyKind.CONCURRENT)


    # region impl

    @staticmethod
    def intercepted(func: Callable):
        return func

    @staticmethod
    def subscribeInternal(eventClass: Type[Event], listener: Listener):
        GlobalEventListeners[listener.priority].append(ListenerRegistry(eventClass, listener))
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
