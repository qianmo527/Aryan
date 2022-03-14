import asyncio
from src.aryan import Mirai, MiraiSession, Bot, BotConfiguration
from src.aryan import GlobalEventChannel, EventPriority, ConcurrencyKind, ListeningStatus
from src.aryan import GroupMessage, FriendMessage, MessageEvent
from src.aryan import Plain, Face


app = Mirai(
    MiraiSession(
        verify_key="verifyKey",
        host="localhost:8080",
    ),
    loop=asyncio.new_event_loop(),
    bots=[
        Bot(BotConfiguration(account=1375075223)),
        # Bot(BotConfiguration(account=552282813))
    ]
)


async def main(event: GroupMessage):
    print("listener received event:", type(event))
    await event.reply(str(type(event)))

    # next_event: FriendMessage = await event.bot.eventChannel.nextEvent(FriendMessage)
    # await next_event.reply("True")

# GlobalEventChannel.INSTANCE.filterIsInstance(BotEvent).subscribeOnce(GroupMessage, main)

GlobalEventChannel.INSTANCE.subscribeMessages({
    "签到.*?": "签到成功!!!",
    "test": Plain("received"),
    "hello world": [Plain("这是联合消息"), Face(176)],
    "test2": lambda ev: ev.reply("test"),
    "default": "default reply"
}, default=True)


try:
    app.launch_blocking()
except KeyboardInterrupt:
    pass
