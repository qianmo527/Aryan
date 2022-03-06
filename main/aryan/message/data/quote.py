from .single_message import MessageMetadata
from ..code.codable import CodableMessage
from .chain import MessageChain


class Quote(MessageMetadata, CodableMessage):
    type: str = "Quote"
    id: int
    senderId: int
    targetId: int
    groupId: int = 0
    origin: MessageChain

    def contentToString(self) -> str:
        return f"[mirai:quote:[{self.id}]]"

    def serializeToMiraiCode(self) -> str:
        return f"[mirai:quote:[{self.id}]]"

    def equals(self, other) -> bool:
        return type(other) is Quote and self.id == other.id
