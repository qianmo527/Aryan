from dataclasses import dataclass
from aiohttp import ClientSession
from loguru import logger


@dataclass
class MiraiSession:
    verify_key: str
    qq: int
    host: str

class MiraiProtocol:
    verify_session: str
    session: ClientSession
    connect_info: MiraiSession

    def __init__(self, session: MiraiSession):
        self.connect_info = session
        self.session = ClientSession()

    async def verify(self):
        async with self.session.post(f"http://{self.host}:{self.port}/verify", json={"verifyKey": self.verify_key}) as verify_response:
            verify_response.raise_for_status()
            self.verify_session = (await verify_response.json())["session"]
        async with self.session.post(f"http://{self.host}:{self.port}/bind", json={"sessionKey": self.verify_session, "qq": self.qq}) as bind_response:
            bind_response.raise_for_status()
            logger.info("http session activated successfully")

    async def release(self):
        async with self.session.post(f"http://{self.host}:{self.port}/release", json={"sessionKey": self.verify_session, "qq": self.qq}):
            pass
