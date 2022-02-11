from datetime import datetime
from pydantic import Field


from .member import Member


class NormalMember(Member):
    name: str = Field(..., alia="memberName")
    specialTitle: str
    muteTimeRemaining: int
    @property
    def isMuted(self) -> bool:
        return not self.id == 0
    joinTimeStamp: datetime
    lastSpeakTimeStamp: datetime

    def unmute(self):
        pass
    def kick(self):
        pass
    def modifyAdmin(self, operation: bool):
        pass

    from ..message.data.message import Message
    from ..message.message_receipt import MessageReceipt
    def sendMessage(self, message: Message) -> MessageReceipt["NormalMember"]:
        pass
    def sendMessage(self, message: str) -> MessageReceipt["NormalMember"]:
        pass
    def nudge(self):
        pass

    def nameCardOrNick(self):
        pass

    def mute(self):
        pass
