import asyncio
from main import Mirai, MiraiSession, Bot, BotConfiguration
from main import GlobalEventChannel, EventPriority, ConcurrencyKind, ListeningStatus
from main import GroupMessage, FriendMessage


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


async def main(event: FriendMessage):
    # bot = app.getBot(1375075223)
    # await app.sendFriendMessage(bot, event.sender, "hello")
    await event.quoteReply("hello world")

GlobalEventChannel.INSTANCE.subscribeAlways(FriendMessage, main)

app.launch_blocking()
