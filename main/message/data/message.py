from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, overload
from pydantic import BaseModel

if TYPE_CHECKING:
    from ...contact import Contact


class Message(BaseModel, metaclass=ABCMeta):

    @property
    def content(self) -> str:
        return self.contentToString()

    @abstractmethod
    def toString(self) -> str: ...

    @abstractmethod
    def contentToString(self) -> str: ...

    def contentEquals(self, another: "Message", ignore_case: bool=False, strict: bool=False) -> bool:
        """判断内容是否与 [another] 的 [contentToString()] 相等

        Args:
            ignore_case (bool, optional): 为True时忽略大小写. Defaults to False.
            strict (bool, optional): 为True时，额外判断每个消息元素的类型，顺序和属性. 如 [Image] 会
            判断 [Image.imageId]. Defaults to False.
        """
        pass  # TODO Implement

    def followedBy(self, tail: "Message"): pass
    @overload
    def plus(self): pass  # TODO

    def sendTo(self, contact: Contact, message): pass  # TODO

    def isContentEmpty(self): pass  # 这两个好像作为Property更好一点
    def isContentBlank(self): pass
