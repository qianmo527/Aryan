import aiohttp
from aiohttp import WSMsgType
import asyncio
import json
from typing import TYPE_CHECKING, Optional, TypeVar, Generic, Dict, overload, List
from loguru import logger
import pickle


from .protocol import MiraiProtocol, MiraiSession
from .event.events.bot import BotEvent
from .event import Event

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
    def parse_event(obj: Dict):
        # TODO: http adapter message parse
        if "type" in obj and isinstance(obj, dict):
            for i in Mirai.all_event_generator():
                if i.__name__ == obj["type"]:
                    return i.parse_obj({k: v for k, v in obj.items() if k != "type"})

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
                    event = self.parse_event(data["data"])
                    if event:
                        self.log_formatter(event, bot)
                elif ws_message.type == WSMsgType.CLOSED:
                    # self.logger.info("websocket connection has closed")
                    # TODO: 倒计时等待重连 结束断开
                    ...

    def log_formatter(self, event: Event, bot: "Bot"):
        from .event.events.message import FriendMessage, GroupMessage, TempMessage
        if isinstance(event, FriendMessage):
            self.logger.info(
                f"Bot.{bot.configuration.account}: {event.sender.nickname}({event.sender.id}) -> "\
                f"{event.messageChain.serializeToMiraiCode()}"
            )
        elif isinstance(event, GroupMessage):
            self.logger.info(
                f"Bot.{bot.configuration.account}: [{event.sender.group.name}({event.sender.group.id})] "\
                f"{event.sender.name}({event.sender.id}) -> {event.messageChain.serializeToMiraiCode()}"
            )
        elif isinstance(event, TempMessage):
            self.logger.info(
                f"Bot.{bot.configuration.account}: [{event.sender.group.name}({event.sender.group.id})] "\
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
        self.logger.info("aryan shutdowned")

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

    # TODO: 其实可以合并的
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
            self.url_root(f"about")
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

    async def sendFriendMessage(self):
        async with self.session.post(
            self.url_root("sendFriendMessage"),
            json={
                "sessionKey": self.http_session or self.ws_session,
                "target": 2816661524,
                "messageChain": [{"type":"Plain", "text": "hello world"}]
            }
        ) as response:
            response.raise_for_status()
            print(await response.json())

    async def sendGroupMessage(self):
        async with self.session.post(
            self.url_root("sendGroupMessage"),
            json={
                "sessionKey": self.http_session,
                "target": 954539214,
                "messageChain": [{ "type":"Plain", "text":"hello " },{ "type":"Plain", "text":"world" }]
            }
        ) as response:
            response.raise_for_status()
            print(await response.json())
