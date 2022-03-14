from .single_message import MessageContent
from ..code.codable import CodableMessage


class Face(MessageContent, CodableMessage):
    type: str = "Face"
    faceId: int
    name: str

    def __init__(self, faceId: int, name: str="", *_, **__):
        super().__init__(faceId=faceId, name=name)

    def contentToString(self) -> str:
        return f"[{self.name or '表情'}]"

    def equals(self, other) -> bool:
        return type(other) is Face and other.faceId == self.faceId

    def serializeToMiraiCode(self):
        return f"[mirai:face:{self.faceId}]"
