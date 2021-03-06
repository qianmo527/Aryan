from typing import NoReturn
from pydantic import BaseModel, Extra
from abc import ABCMeta, abstractmethod


class Event(BaseModel, metaclass=ABCMeta):

    @property
    def isIntercepted(self): pass  # 事件是否已被拦截 所有监听器都可以拦截事件 拦截后低优先级的监听器将不会收到这个事件

    @property
    def isCancelled(self): pass

    def intercept(self) -> NoReturn: pass

    async def broadcast(self): pass

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(" + ", ".join(
            (
                f"{k}={repr(v)}"
                for k, v in self.__dict__.items() if k != "type" and v
            )
        ) + ")"


class CancellableEvent(metaclass=ABCMeta):
    """取消这个事件
    事件需实现 [CancellableEvent] Mix-in才可以被取消 否则属性 [isCancelled] 固定返回False

    Raises:
        AssertionError: 当事件未实现Mix-in [CancellableEvent] 并调用 [Event.cancel()] 时抛出
    """

    @property
    def isCancelld(self): pass

    def cancel(self): pass


class AbstractEvent(Event):
    """所有实现了 [Event] Mix-in的类都应该继承的父类
    在使用事件时应使用类型 [Event]. 在实现自定义事件时应继承 [AbstractEvent]
    """

    _intercepted: bool = False
    _cancelled: bool = False

    @property
    def isIntercepted(self) -> bool:
        return self._intercepted

    @property
    def isCancelled(self):
        return self._cancelled

    def intercept(self) -> NoReturn:
        """拦截事件 不向低优先级监听器传播"""
        self._intercepted = True

    def cancel(self) -> NoReturn:
        assert isinstance(self, CancellableEvent)
        self._cancelled = True

    async def broadcast(self):
        from .channel import GlobalEventChannel
        return await GlobalEventChannel.INSTANCE.broadcast(self)
