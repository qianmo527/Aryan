import asyncio
from main.aryan import Mirai, MiraiSession, Bot, BotConfiguration
from main.aryan import GlobalEventChannel, EventPriority, ConcurrencyKind, ListeningStatus
from main.aryan import GroupMessage, FriendMessage
from main.aryan import BotEvent



app = Mirai(
    MiraiSession(
        verify_key="verifyKey",
        host="localhost:8080",
    ),
    loop=asyncio.get_event_loop(),
    bots=[
        Bot(BotConfiguration(account=1375075223)),
        # Bot(BotConfiguration(account=552282813))
    ]
)


async def main(event: GroupMessage):
    print("listener received event:", event.__class__.__name__)

GlobalEventChannel.INSTANCE.filter(lambda event: isinstance(event, BotEvent)).subscribeAlways(GroupMessage, main)

try:
    app.launch_blocking()
except KeyboardInterrupt:
    pass
