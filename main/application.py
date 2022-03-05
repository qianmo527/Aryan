import aiohttp
from aiohttp import WSMsgType
import asyncio
import json
from typing import TYPE_CHECKING, Optional, TypeVar, Generic, Dict, overload, List, Optional, Union
from loguru import logger
import pickle


from .protocol import MiraiProtocol, MiraiSession
from .event.events.bot import BotEvent
from .event import Event
from .message.data.chain import MessageChain
from .message.data.source import Source
from .contact.friend import Friend
from .contact.group import Group
from .contact.member import Member

if TYPE_CHECKING:
    from .bot import Bot
    from .contact.contact import Contact


class Mirai(MiraiProtocol):
    """与Mirai进行交互的接口类
    """
    __instance: "Mirai" = None
    loop: asyncio.AbstractEventLoop
    logger = logger
    bots: List["Bot"] = []

    def __init__(self, session: MiraiSession, loop: Optional[asyncio.AbstractEventLoop]=None, bots: List["Bot"]=[]):
        super().__init__(connect_info=session, bots=bots)
        self.loop = loop or asyncio.get_event_loop()
        Mirai.__instance = self
        for bot in bots:
            bot.application = self

    @classmethod
    def getInstance(cls):
        if cls.__instance:
            return cls.__instance
        else:
            return None

    def url_root(self, path: str, bot: "Bot"):
        return "{}://{}/{}".format("ws" if bot.configuration.ws_session else "http", self.connect_info.host, path)

    @staticmethod
    def all_event_generator(base=BotEvent):
        for i in base.__subclasses__():
            yield i
            if i.__subclasses__():
                yield from Mirai.all_event_generator(i)

    @staticmethod
    def parse_event(obj: Dict, bot: "Bot"):
        from .contact.contact_or_bot import ContactOrBot
        # TODO: http adapter message parse
        if "type" in obj and isinstance(obj, dict):
            for i in Mirai.all_event_generator():
                if i.__name__ == obj["type"]:
                    event = i.parse_obj({k: v for k, v in obj.items() if k != "type"})
                    for name, anno in event.__annotations__.items():
                        if issubclass(anno, ContactOrBot):
                            event.__getattribute__(name).bot = bot
                    return event

    async def ws_all(self, bot: "Bot"):
        async with self.session.ws_connect(
            self.url_root("all", bot) + f"?verifyKey={self.connect_info.verify_key}&qq={bot.configuration.account}"
        ) as connection:
            self.logger.info(f"Bot.{bot.configuration.account} websocket connected successfully")
            while True:
                ws_message = await connection.receive()
                if ws_message.type == WSMsgType.TEXT:
                    data = json.loads(ws_message.data)
                    if not bot.configuration.ws_session:
                        bot.configuration.ws_session = data["data"]["session"]
                    print(data)
                    event = self.parse_event(data["data"], bot=bot)
                    if event:
                        self.log_formatter(event, bot)
                        # TODO: Event.broadcast()
                        from .event.channel import GlobalEventChannel
                        await GlobalEventChannel.INSTANCE.broadcast(event)
                elif ws_message.type == WSMsgType.CLOSED:
                    # self.logger.info("websocket connection has closed")
                    ...

    def log_formatter(self, event: Event, bot: "Bot"):
        from .event.events.message import FriendMessage, GroupMessage, TempMessage
        if isinstance(event, FriendMessage):
            self.logger.info(
                f"Bot.{bot.configuration.account}: {event.sender.nickname}({event.sender.id}) -> "
                f"{event.messageChain.serializeToMiraiCode()}"
            )
        elif isinstance(event, GroupMessage):
            self.logger.info(
                f"Bot.{bot.configuration.account}: [{event.sender.group.name}({event.sender.group.id})] "
                f"{event.sender.name}({event.sender.id}) -> {event.messageChain.serializeToMiraiCode()}"
            )
        elif isinstance(event, TempMessage):
            self.logger.info(
                f"Bot.{bot.configuration.account}: [{event.sender.group.name}({event.sender.group.id})] "
                f"{event.sender.name}(Temp {event.sender.id}) -> {event.messageChain.serializeToMiraiCode()}"
            )
        else:
            self.logger.info(f"Bot.{bot.configuration.account}: Event: {event.__repr__()}")

    async def shutdown(self):
        await self.session.close()
        for t in asyncio.all_tasks(self.loop):
            if t is not asyncio.current_task(self.loop):
                t.cancel()
                try:
                    await t
                except asyncio.CancelledError:
                    pass
        self.logger.info("aryan shutdown")

    def __del__(self):
        self.loop.run_until_complete(self.shutdown())

    async def lifecycle(self):
        self._update_forward_refs()
        await asyncio.gather(*[self.verify(bot) for bot in self.bots])
        # await asyncio.gather(*[bot.init() for bot in self.bots])
        await asyncio.gather(*[self.ws_all(bot) for bot in self.bots])

    @staticmethod
    def _update_forward_refs():
        from .contact.contact_or_bot import ContactOrBot
        from .contact.group import Group
        from .contact.member import Member
        from .bot import Bot
        # TODO: 将所有所属Bot适配
        ContactOrBot.update_forward_refs(Bot=Bot)
        Group.update_forward_refs(Bot=Bot)
        Member.update_forward_refs(Bot=Bot, Group=Group)

    def launch_blocking(self):
        try:
            self.loop.run_until_complete(self.lifecycle())
        except KeyboardInterrupt:
            raise
        finally:
            self.loop.run_until_complete(self.shutdown())

    def getBot(self, account: int):
        for i in self.bots:
            if i.configuration.account == account:
                return i

    C = TypeVar("C", bound="Contact")
    async def getContactList(self, c: Generic[C], bot: "Bot"):
        from .contact.friend import Friend
        from .contact.group import Group
        if c is Friend:
            return self.getFriendList(bot)
        elif c is Group:
            return self.getGroupList(bot)

    async def getAbout(self):
        async with self.session.get(
            self.url_root(f"about", self.bots[0])
        ) as response:
            response.raise_for_status()
            print(await response.json())

    async def getFriendList(self, bot: "Bot"):
        async with self.session.get(
            self.url_root(f"friendList?sessionKey={bot.configuration.http_session or bot.configuration.ws_session}", bot)
        ) as response:
            from .contact.friend import Friend
            response.raise_for_status()
            return [Friend.parse_obj(obj) for obj in (await response.json())["data"]]

    async def getGroupList(self, bot: "Bot"):
        async with self.session.get(
            self.url_root(f"groupList?sessionKey={bot.configuration.http_session or bot.configuration.ws_session}", bot)
        ) as response:
            from .contact.group import Group
            response.raise_for_status()
            return [Group.parse_obj(obj) for obj in (await response.json())["data"]]

    async def sendFriendMessage(self,
        bot: "Bot",
        target: Union[Friend, int],
        message: Union[MessageChain, str],
        quote: Optional[Union[Source, int]]=None
    ):
        # TODO: 支持传入单个Element
        from .message.data.plain import Plain
        async with self.session.post(
            self.url_root("sendFriendMessage", bot),
            json={
                "sessionKey": bot.configuration.http_session or bot.configuration.ws_session,
                "target": target.id if isinstance(target, Friend) else target,
                "messageChain": [i.json() for i in message.__root__] if isinstance(message, MessageChain)
                                else [Plain(message).dict()],
                "quote": quote.id if isinstance(quote, Source) else quote
            }
        ) as response:
            response.raise_for_status()
            print(await response.json())

    async def sendGroupMessage(self,
        bot: "Bot",
        target: Union[Group, int],
        message: Union[MessageChain, str],
        quote: Optional[Union[Source, int]]=None
    ):
        # TODO: 支持传入单个Element
        from .message.data.plain import Plain
        async with self.session.post(
            self.url_root("sendGroupMessage", bot),
            json={
                "sessionKey": bot.configuration.http_session or bot.configuration.ws_session,
                "target": target.id if isinstance(target, Group) else target,
                "messageChain": [i.json() for i in message.__root__] if isinstance(message, MessageChain)
                                else [Plain(message).dict()],
                "quote": quote.id if isinstance(quote, Source) else quote
            }
        ) as response:
            response.raise_for_status()
            print(await response.json())

    async def sendTempMessage(self,
        bot: "Bot",
        target: Union[Member, int],
        message: Union[MessageChain, str],
        quote: Optional[Union[Source, int]]=None,
        group: Optional[Union[Group, int]]=None
    ):
        # TODO: 支持传入单个Element
        from .message.data.plain import Plain
        async with self.session.post(
            self.url_root("sendGroupMessage", bot),
            json={
                "sessionKey": bot.configuration.http_session or bot.configuration.ws_session,
                "qq": target.id if isinstance(target, Member) else target,
                "group": target.group.id if isinstance(target, Member) else
                         group.id if group and isinstance(group, Group) else group,
                "messageChain": [i.json() for i in message.__root__] if isinstance(message, MessageChain)
                                else [Plain(message).dict()],
                "quote": quote.id if isinstance(quote, Source) else quote
            }
        ) as response:
            response.raise_for_status()
            print(await response.json())

    async def sendNudge(self): pass

    async def recall(self, target: Union[Source, int], bot: "Bot"):
        async with self.session.post(
            self.url_root("recall", bot),
            json={
                "sessionKey": bot.configuration.http_session or bot.configuration.ws_session,
                "target": target.id if isinstance(target, Source) else target
            }
        ) as response:
            response.raise_for_status()
            print(await response.json())

    async def deleteFriend(self, target: Union[Friend, int], bot: "Bot"):
        async with self.session.post(
            self.url_root("deleteFriend", bot),
            json={
                "sessionKey": bot.configuration.http_session or bot.configuration.ws_session,
                "target": target.id if isinstance(target, Friend) else target
            }
        ) as response:
            response.raise_for_status()
            print(await response.json())
