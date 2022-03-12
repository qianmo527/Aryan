from abc import ABCMeta, abstractmethod
from typing import List
import re

from ..data.chain import MessageChain

class MiraiCode:

    @classmethod
    def __new__(cls: type["MiraiCode"], *args, **kwargs) -> "MiraiCode":
        raise Exception("无法实例化 [MiraiCode] 类 请使用[MiraiCode.deserializeMiraiCode()")
        return object.__new__(cls)

    @staticmethod
    def deserializeMiraiCode(content: str) -> MessageChain:
        """ 由mirai码字符串取得 [MessageChain] 实例

        Args:
            content (str): mirai码字符串

        Raises:
            ValueError: 无法识别mirai码时抛出
        """

        from ..data.message import Message
        from ..data.single_message import SingleMessage, MessageContent, MessageMetadata
        from ..data.plain import Plain

        # "[mirai:atall]Plain[mirai:at:123]这是一个Plain"
        element_list = [i for i in re.split(r"(\[mirai:.+?\])", content) if not i == ""]
        # ["[mirai:atall"], "Plain", "[mirai:at:123]", "这是一个Plain"]
        instance: List[SingleMessage] = []
        for i in element_list:
            if not i.startswith("[mirai:"):
                instance.append(Plain(i.replace("[_", "[")))
            else:
                # TODO 解析出类型和参数
                from ..data.single_message import MessageMetadata, MessageContent
                # element_type: str = re.


        raise ValueError("无法识别的mirai码 " + content)
