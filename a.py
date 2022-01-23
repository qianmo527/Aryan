import asyncio
from dataclasses import dataclass

from main.protocol import MiraiSession
from main import Mirai


loop = asyncio.get_event_loop()
mirai = Mirai(MiraiSession(verify_key="verifyKey", qq=552282813, host="localhost:8080"), loop)

mirai.launch_blocking()
