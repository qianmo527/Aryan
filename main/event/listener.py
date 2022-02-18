"""事件监听器"""
import asyncio
from enum import Enum
from typing import Dict, List, Type
from types import FunctionType


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

    MONITOR = 0,
    "使用此优先级的监听器应遵守约束 不拦截事件"


class Listener:
    concurrencyKind: ConcurrencyKind
    priority: EventPriority

    def __init__(self, priority: EventPriority=EventPriority.MONITOR,
                 concurrencyKind: ConcurrencyKind=ConcurrencyKind.CONCURRENT):
        self.concurrencyKind = concurrencyKind
        self.priority = priority

    def onEvent(self) -> ListeningStatus:
        pass

    def complete(self):
        """结束监听"""

    @staticmethod
    def createListener(
        handler: FunctionType,
        concurrencyKind: ConcurrencyKind,
        priority: EventPriority=EventPriority.NORMAL
    ):
        return Listener()


class ListenerRegistry:
    event: Type[Event]
    listener: Listener


class GlobalEventListeners:
    ALL_LEVEL_REGISTRIES: Dict[EventPriority, List[ListenerRegistry]]

    def __init__(self):
        self.ALL_LEVEL_REGISTRIES = {priority: [] for priority in EventPriority}

    def get(self, priority: EventPriority):
        """返回优先级priority对应的监听器列表"""
        return self.ALL_LEVEL_REGISTRIES[priority]

    def __getitem__(self, priority: EventPriority):
        return self.ALL_LEVEL_REGISTRIES[priority]

    def __contains__(self, item):
        return item in self.ALL_LEVEL_REGISTRIES.values()


class ListenerHostInterface:  # TODO: 把这个骚里骚气的东西写了谢谢 | 强大的扩展性

    def EventHandler(self): pass


class SimpleListenerHost(ListenerHostInterface):
    pass


async def process(
    container: List[ListenerRegistry],
    registry: ListenerRegistry,
    listener: Listener,
    event: Event
):
    if listener.concurrencyKind == ConcurrencyKind.LOCKED:
        pass
    elif listener.concurrencyKind == ConcurrencyKind.CONCURRENT:
        pass
