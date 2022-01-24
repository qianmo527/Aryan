from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .single_message import MessageContent
    from ..code.codable import CodableMessage


class At(MessageContent, CodableMessage):
    type = "At"
    target: int
    # display: str

    def contentToString(self) -> str:
        return f"@{self.target}"

    def serializeToMiraiCode(self):
        return f"[mirai:at:{self.target}]"

class AtAll(MessageContent, CodableMessage):
    type = "AtAll"
    display: str = "@全体成员"
