from typing import NoReturn
from pydantic import BaseModel
from abc import ABCMeta, abstractmethod


class Event(BaseModel, metaclass=ABCMeta):

    @property
    def isIntercepted(self): pass # 事件是否已被拦截 所有监听器都可以拦截事件 拦截后低优先级的监听器将不会收到这个事件

    @abstractmethod
    def intercept(self) -> NoReturn: pass

    class Config:
        arbitrary_types_allowed = True


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

    __intercepted: bool = False
    __cancelled: bool = False

    @property
    def isIntercepted(self) -> bool:
        return self.__intercepted

    @property
    def isCancelled(self):
        return self.__cancelled

    def intercept(self) -> NoReturn:
        """拦截事件 不向低优先级监听器传播"""
        self.__intercepted = True

    def cancel(self) -> NoReturn:
        assert self is CancellableEvent
        self.__cancelled = True
