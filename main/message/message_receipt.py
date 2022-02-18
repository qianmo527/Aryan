from typing import TYPE_CHECKING, TypeVar, Generic

if TYPE_CHECKING:
    from ..contact.contact import Contact
    from .data.source import Source
    from .data.chain import MessageChain
    from ..bot import Bot
from ..contact.contact import Contact


T = TypeVar("T", bound=Contact)

class MessageReceipt(Generic[T]): 
    """发送消息后得到的回执. 可用于撤回, 引用回复等
    """
    source: "Source"  # 指代发送出去的消息
    target: T  # 发送目标 为 [Group] 或 [Friend] 或 [Member]
    bot: "Bot"
    origin_message: "MessageChain"
    

    def __init__(self, source: "Source", target: T):
        self.source = source
        self.target = target
        self.bot = target.bot
        # TODO 获取源消息
        from ..application import Mirai
        app = Mirai.getInstance()


    @property
    def isToGroup(self):
        """是否为发送给群的消息的回执"""
        from ..contact.group import Group
        return isinstance(self.target, Group)

    def recall(self):
        """撤回这条消息"""
        pass

    def recallIn(self, time: float):
        """在一段时间后撤回这条消息"""
        pass

