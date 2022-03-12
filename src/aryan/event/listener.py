"""事件监听器"""
import asyncio
from asyncio import Lock
from enum import Enum
from typing import Dict, List, Type, Callable

from . import Event


class ListeningStatus(Enum):
    """订阅者的状态"""

    LISTENING = 1,  
    "表示继续监听"

    STOPPED = 0 
    "表示已停止."


class ConcurrencyKind(Enum):
    CONCURRENT = 1,
    LOCKED = 0


class EventPriority(Enum):
    """事件优先级

    在广播时, 事件监听器的调用顺序为 (从左到右):\n
    [HIGHEST] -> [HIGH] -> [NORMAL] -> [LOW] -> [LOWEST] -> [MONITOR]

    - 使用 [MONITOR] 优先级的监听器将会被**并发**调用.\n
    - 使用其他优先级的监听器都将会**按顺序**调用.\n
    因此一个监听器的挂起可以阻塞事件处理过程而导致低优先级的监听器较晚处理.

    当事件被 [拦截][Event.intercept] 后, 优先级较低 (靠右) 的监听器将不会被调用.
    """

    HIGHEST = 5,
    HIGH = 4,
    NORMAL = 3,
    LOW = 2,
    LOWEST = 1,

    MONITOR = 0
    "使用此优先级的监听器应遵守约束 不拦截事件"

    @classmethod
    @property
    def prioritiesExcludedMonitor(cls) -> list:
        return [priority for priority in cls if not priority == cls.MONITOR]


class Listener:
    concurrencyKind: ConcurrencyKind
    priority: EventPriority

    def __init__(self, priority: EventPriority=EventPriority.NORMAL,
                 concurrencyKind: ConcurrencyKind=ConcurrencyKind.CONCURRENT):
        self.concurrencyKind = concurrencyKind
        self.priority = priority

    async def onEvent(self, event: Event) -> ListeningStatus:
        pass

    def complete(self):
        """结束监听"""


class ListenerRegistry:
    type: Type[Event]
    listener: Listener

    def __init__(self, type: Type[Event], listener: Listener):
        self.type = type
        self.listener = listener


class GlobalEventListeners(dict):
    def __init__(self):
        super().__init__({priority: [] for priority in EventPriority})
GlobalEventListeners = GlobalEventListeners()


class ListenerHostInterface:  # TODO: 强大的扩展性

    def EventHandler(self): pass  # annotation
class SimpleListenerHost(ListenerHostInterface):
    pass


class Handler(Listener):
    """事件处理器"""
    handler: Callable[..., ListeningStatus]
    priority: EventPriority
    concurrencyKind: ConcurrencyKind

    def __init__(self, handler: Callable[..., ListeningStatus], priority: EventPriority, concurrencyKind: ConcurrencyKind):
        self.handler = handler
        super().__init__(priority, concurrencyKind)

    async def onEvent(self, event: Event) -> ListeningStatus:
        if event.isCancelled: return ListeningStatus.STOPPED
        status = await self.handler(event)
        if status == ListeningStatus.STOPPED:
            return ListeningStatus.STOPPED
        else:
            return ListeningStatus.LISTENING


async def callAndRemoveIfRequired(event: Event):
    for p in EventPriority.prioritiesExcludedMonitor:
        container: List[ListenerRegistry] = GlobalEventListeners[p]
        task_queue = []
        for registry in container:
            if event.isIntercepted: return
            if not isinstance(event, registry.type): continue
            listener = registry.listener
            task_queue.append(asyncio.create_task(process(container, registry, listener, event)))
        for task in task_queue:
            await task

    if event.isIntercepted: return
    container: List[ListenerRegistry] = GlobalEventListeners[EventPriority.MONITOR]
    # switch(match) area
    if len(container) == 0: return
    elif len(container) == 1:
        registry: ListenerRegistry = container[0]
        if not isinstance(event, registry.type): return
        await process(container, registry, registry.listener, event)
    else:
        task_queue = []
        for registry in container:
            if not isinstance(event, registry.type): continue
            task_queue.append(asyncio.get_running_loop().create_task(process(container, registry, registry.listener, event)))
        await asyncio.wait(task_queue)

lock = Lock()

async def process(
    container: List[ListenerRegistry],
    registry: ListenerRegistry,
    listener: Listener,
    event: Event
):
    if listener.concurrencyKind == ConcurrencyKind.LOCKED:
        async with lock:
            if await listener.onEvent(event) == ListeningStatus.STOPPED:
                container.remove(registry)
    elif listener.concurrencyKind == ConcurrencyKind.CONCURRENT:
        if await listener.onEvent(event) == ListeningStatus.STOPPED:
            container.remove(registry)
