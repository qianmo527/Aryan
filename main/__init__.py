import aiohttp
from aiohttp import WSMsgType
import asyncio
import json
from typing import Optional
from loguru import logger


from .protocol import MiraiProtocol, MiraiSession


class Mirai(MiraiProtocol):
    loop: asyncio.AbstractEventLoop
    logger = logger

    def __init__(self, session: MiraiSession, loop: Optional[asyncio.AbstractEventLoop]=None):
        super().__init__(session)
        self.loop = loop or asyncio.get_event_loop()

    def url_root(self, path: str, type: str):
        return f"{type}://{self.connect_info.host}/{path}"

    async def ws_all(self):
        async with self.session.ws_connect(
            self.url_root("all", "ws") + f"?verifyKey={self.connect_info.verify_key}&qq={self.connect_info.qq}"
        ) as connection:
            self.logger.info("websocket connected successfully")
            while True:
                ws_message = await connection.receive()
                if ws_message.type == WSMsgType.TEXT:
                    data = json.loads(ws_message.data)
                    print(data)

    async def shutdown(self):
        await self.session.close()
        for t in asyncio.all_tasks(self.loop):
            if t is not asyncio.current_task(self.loop):
                t.cancel()
                try:
                    await t
                except asyncio.CancelledError:
                    pass
        self.logger.info("aryan is closed")

    async def lifecycle(self):
        await self.ws_all()

    def launch_blocking(self):
        try:
            self.loop.run_until_complete(self.lifecycle())
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.run_until_complete(self.shutdown())