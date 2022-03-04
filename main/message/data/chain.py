from typing import List, TYPE_CHECKING, Sequence, Type


from .message import Message
from ..code.codable import CodableMessage

if TYPE_CHECKING:
    from .single_message import SingleMessage
from .single_message import SingleMessage


class MessageChain(CodableMessage, Message):
    """MessageChain（消息链） 是 List[SingleMessage.主动发送的消息和从服务器接收消息都是 MessageChain
    """

    __root__: Sequence[SingleMessage]

    @staticmethod
    def build_chain(obj):
        from .single_message import MessageMetadata, MessageContent
        elements = []
        for i in obj:
            for ii in MessageMetadata.__subclasses__():
                if i["type"] == ii.__name__:
                    elements.append(ii.parse_obj(i))
                    break
            for ii in MessageContent.__subclasses__():
                if i["type"] == ii.__name__:
                    elements.append(ii.parse_obj(i))
                    break
        return elements

    @classmethod
    def parse_obj(cls, obj: List["SingleMessage"]) -> "MessageChain":
        return cls(__root__=cls.build_chain(obj))

    def __init__(self, __root__):
        super().__init__(__root__=self.build_chain(__root__))

    def get(self, element: Type["SingleMessage"]) -> List["SingleMessage"]:
        return [i for i in self.__root__ if isinstance(i, element)]

    def getFirst(self, element: Type["SingleMessage"]) -> "SingleMessage":
        return self.get(element)[0]

    def serializeToMiraiCode(self) -> str:
        """将 [MessageChain] 转换为 "mirai码" 表示的字符串\n
        为保证可逆，将 [Plain] 中的 "[" 用 "[_" 代替
        """
        from ..code.codable import CodableMessage
        return "".join([i.serializeToMiraiCode() for i in self.__root__ if isinstance(i, CodableMessage)])

    def contentToString(self) -> str:
        return "".join([i.contentToString() for i in self.__root__])

    @classmethod
    def deserializeMiraiCode(cls, content: str) -> "MessageChain":
        from ..code.mirai_code import MiraiCode
        return MiraiCode.deserializeMiraiCode(content)

    def __repr__(self) -> str:
        return f"MessageChain({self.__root__})"

    def __str__(self) -> str:
        return f"MessageChain({self.__root__})"

    def has(self, type: "SingleMessage"):
        return self.__contains__(type)

    def __contains__(self, obj_type: object) -> bool:
        return obj_type in [type(i) for i in self.__root__]
