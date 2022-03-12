from dataclasses import dataclass
from aiohttp import ClientSession
from loguru import logger
from typing import TYPE_CHECKING, List
import asyncio

if TYPE_CHECKING:
    from .bot import Bot


@dataclass
class MiraiSession:
    verify_key: str
    host: str

class MiraiProtocol:
    session: ClientSession
    connect_info: MiraiSession
    bots: List["Bot"] = []
    loop: asyncio.AbstractEventLoop

    def __init__(self, connect_info: MiraiSession, loop, bots: List=[]):
        self.loop = loop or asyncio.new_event_loop()
        self.connect_info = connect_info
        self.session = ClientSession(loop=self.loop)
        from .bot import Bot
        self.bots = (bots, [bots])[isinstance(bots, Bot)]

    async def verify(self, bot: "Bot"):
        # TODO: http adapter 未开启的处理
        async with self.session.post(f"http://{self.connect_info.host}/verify", json={"verifyKey": self.connect_info.verify_key}) as verify_response:
            verify_response.raise_for_status()
            bot.configuration.http_session = (await verify_response.json())["session"]
        async with self.session.post(f"http://{self.connect_info.host}/bind", json={"sessionKey": bot.configuration.http_session, "qq": bot.configuration.account}) as bind_response:
            bind_response.raise_for_status()
            logger.info(f"Bot.{bot.configuration.account} http session activated successfully")

    async def release(self, bot: "Bot"):
        async with self.session.post(f"http://{self.connect_info.host}/release", json={"sessionKey": bot.configuration.http_session, "qq": bot.configuration.account}) as response:
            response.raise_for_status()
            logger.info(f"Bot.{bot.configuration.account} http session released")
