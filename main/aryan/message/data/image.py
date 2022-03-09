from enum import Enum

from .single_message import MessageContent
from ..code.codable import CodableMessage


class UploadMethod(Enum):
    Friend = "friend"
    Group = "group"
    Temp = "temp"



class Image(MessageContent, CodableMessage):
    type: str = "Image"
    imageId: str
    url: str
    path: str = None
    base: str = None

    def contentToString(self) -> str:
        return "[图片]"

    def serializeToMiraiCode(self):
        return f"[mirai:image:{self.imageId}]"

    @staticmethod
    def uploadImage(data: bytes, method: UploadMethod, bot):
        return bot.uploadImage(data, method)

    def asFlash(self) -> "FlashImage":
        return FlashImage.parse_obj({**self.dict(), "type": "FlashImage"})

class FlashImage(Image):
    type: str = "FlashImage"

    def asNormal(self) -> "Image":
        return Image.parse_obj({**self.dict(), type: "Image"})
