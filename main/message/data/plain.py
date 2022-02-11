from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from .single_message import MessageContent
from ..code.codable import CodableMessage



class Plain(MessageContent, CodableMessage):
    type: str = "Plain"
    text: str

    def __init__(self, text: str, *_, **__):
        super().__init__(text=text)

    def contentToString(self) -> str:
        return self.text

    def serializeToMiraiCode(self) -> str:
        """为保证可逆，将 "[" 用 "[_" 代替"""
        return self.text.replace("[", "[_")

    def __repr__(self) -> str:
        return f"Plain({self.text})"

    def __str__(self) -> str:
        return f"Plain({self.text})"
