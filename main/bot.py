from typing import Generic, List, TYPE_CHECKING, TypeVar
from dataclasses import dataclass, field

from .protocol import MiraiSession
from .contact.user_or_bot import UserOrBot
from .contact.contact import Contact

if TYPE_CHECKING:
    from .contact.group import Group
    from .contact.friend import Friend
    from .contact.stranger import Stranger
from .application import Mirai


@dataclass
class BotConfiguration:
    account: int
    password: str
    http_session: str = field(default=None, init=False)
    ws_session: str = field(default=None, init=False)


class Bot(UserOrBot):
    configuration: BotConfiguration  # Bot配置
    isOnline: bool = True # 当 Bot 在线 (可正常收发消息) 时返回 True
    eventChannel: str = None # 来自这个 Bot 的 BotEvent 的事件通道  TODO
    otherClients: List = []  # 其他设备列表  还没写|不打算写 一般情况为空
    # asFriend: Friend # User.id 与 Bot.id 相同的 Friend 实例
    # asStranger: Stranger # User.id 与 Bot.id 相同的 Stranger 实例
    application: "Mirai" = None  # 该 [Bot] 所属于的Application实例

    def __init__(self, configuration: BotConfiguration):
        from .contact.friend import Friend
        from .contact.stranger import Stranger
        super().__init__(
            id=configuration.account, configuration=configuration, asFriend=Friend(id=configuration.account),
            asStranger=Stranger(id=configuration.account), isOnline=True
        )

    def init(self):
        """初始化Bot信息
        """

    friends: List["Friend"] = [] # 好友列表 与服务器同步更新
    def getFriend(self, id: int):
        for i in self.friends:
            if id == i.id:
                return i

    def getFriendOrFail(self, id: int):
        pass
    def containsFriend(self, id: int):
        pass

    groups: List["Group"] = []
    def getGroup(self, id: int):
        pass
    def getGroupOrFail(self, id: int):
        pass
    def containsGroup(self, id: int):
        pass
    

    def login(self, connect_info: MiraiSession=None):
        """单Bot启动方式"""
        from .application import Mirai
        instance = Mirai.getInstance()
        # TODO: 快把这个跟shit一样的代码改了 球球了
        if instance:
            instance.bots.append(self)
            instance.loop.run_until_complete(instance.verify(self))
            instance.loop.run_until_complete(instance.ws_all(self))
        elif not instance and connect_info:
            self.application = Mirai(session=connect_info, bots=[self])
            self.application.launch_blocking()
        else:
            raise

    def close(self):
        pass

    """以下为与mirai api交互的地区"""
    async def getAbout(self):
        if self.application:
            return await self.application.getAbout()

    C = TypeVar("C", bound=Contact)
    async def getContactList(self, c: Generic[C]):
        if self.application:
            return await self.application.getContactList(c, self)

    async def getFriendList(self):
        if self.application:
            return await self.application.getFriendList(self)

    async def getGroupList(self):
        if self.application:
            return await self.application.getGroupList(self)

    def __repr_args__(self):
        return [(None, self.configuration.account)]
