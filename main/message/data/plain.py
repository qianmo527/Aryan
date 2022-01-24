from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .single_message import MessageContent
    from ..code.codable import CodableMessage



class Plain(MessageContent, CodableMessage):
    type = "Plain"
    content: str

    def __init__(self, content: str):
        super().__init__(content=content)

    def contentToString(self) -> str:
        return self.content

    def serializeToMiraiCode(self) -> str:
        return self.content
