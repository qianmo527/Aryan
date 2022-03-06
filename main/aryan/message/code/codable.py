from abc import ABCMeta, abstractmethod

from ..data.message import Message


class CodableMessage(Message, metaclass=ABCMeta):
    """可以使用 mirai 码表示的 [Message] 类型
    
    从字符串解析 mirai 码: [MiraiCode.deserializeMiraiCode()]
    
    不适合第三方实现
    """

    @abstractmethod
    def serializeToMiraiCode(self): ...
