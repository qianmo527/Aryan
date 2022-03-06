from pydantic import Field

from .user import User

class Friend(User):
    """代表一位好友

    一个 Friend 实例并不是独立的，它属于一个 Bot\n
    对于同一个 Bot，任何一个人的 Friend 实例都是单一的
    """
    id: int
    nickname: str = ""
    remark: str = ""

    from ..message.data.message import Message
    from ..message.message_receipt import MessageReceipt
    def sendMessage(self, message: Message) -> MessageReceipt["Friend"]:
        pass

    def delete(self):
        """删除并屏蔽该好友 屏蔽后对方将无法发送临时对话消息
        
        FriendDeleteEvent 好友删除事件
        """
        pass

    def nudge(self):
        pass

    def __repr__(self) -> str:
        return f"Friend({self.id}, nickname={self.nickname}, remark={self.remark})"

    def __str__(self) -> str:
        return f"Friend({self.id}, nickname={self.nickname}, remark={self.remark})"
