from abc import ABCMeta, abstractmethod, abstractproperty
from typing import TYPE_CHECKING, overload
from pydantic import BaseModel, BaseConfig, Extra
from datetime import datetime


if TYPE_CHECKING:
    from ...contact import Contact


class Message(BaseModel, metaclass=ABCMeta):

    class Config(BaseConfig):
        extra = Extra.allow
        json_encoders = {
            datetime: lambda v: v.timestamp()
        }

    @property
    def content(self) -> str:
        return self.contentToString()

    # @abstractmethod  TODO
    def contentToString(self) -> str: ...

    def contentEquals(self, another: "Message", ignore_case: bool=False, strict: bool=False) -> bool:
        """判断内容是否与传入 [another] 的 [contentToString()] 相等

        Args:
            ignore_case (bool, optional): 为True时忽略大小写. Defaults to False.
            strict (bool, optional): 为True时，额外判断每个消息元素的类型，顺序和属性. 如 [Image] 会
            判断 [Image.imageId]. Defaults to False.
        """
        if not ignore_case and not strict:
            return self.contentToString() == another.contentToString()
        elif ignore_case and not strict:
            return self.contentToString().lower() == another.contentToString().lower()
        elif not ignore_case and strict:
            pass
        else:
            pass

    def followedBy(self, tail: "Message"): pass  # TODO
    @overload
    def plus(self, obj):  # TODO
        raise TypeError("Not supported type")

    def sendTo(self, contact: "Contact", message): pass  # TODO

    @property
    def isContentEmpty(self):
        return False
    @property
    def isContentBlank(self):
        return False
