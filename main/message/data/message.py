from abc import ABCMeta, abstractmethod
from typing import overload, TYPE_CHECKING

if TYPE_CHECKING:
    from ...contact import Contact


class Message(metaclass=ABCMeta):

    @property
    def content(self) -> str:
        return self.contentToString()

    @abstractmethod
    def toString(self) -> str: ...

    @abstractmethod
    def contentToString(self) -> str: ...

    def contentEquals(self, another: "Message", ignore_case: bool=False, strict: bool=False):
        pass  # TODO

    def followedBy(self, tail: "Message"): pass
    def plus(self): pass  # TODO

    def sendTo(self, contact: Contact, message): pass  # TODO

    def isContentEmpty(self): pass  # 这两个好像作为Property更好一点
    def isContentBlank(self): pass
