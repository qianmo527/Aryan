import asyncio
from main.aryan import Mirai, MiraiSession, Bot, BotConfiguration
from main.aryan import GlobalEventChannel, EventPriority, ConcurrencyKind, ListeningStatus
from main.aryan import GroupMessage, FriendMessage, MessageEvent
from main.aryan import BotEvent, FriendInputStatusChangedEvent



app = Mirai(
    MiraiSession(
        verify_key="verifyKey",
        host="localhost:8080",
    ),
    loop=asyncio.get_event_loop(),
    bots=[
        # Bot(BotConfiguration(account=1375075223)),
        Bot(BotConfiguration(account=552282813))
    ]
)


async def main(event: GroupMessage):
    print("listener received event:", type(event))
    await event.reply(str(type(event)))

    next_event: FriendMessage = await event.bot.eventChannel.nextEvent(FriendMessage)
    await next_event.reply("True")

# GlobalEventChannel.INSTANCE.filterIsInstance(BotEvent).subscribeOnce(FriendInputStatusChangedEvent, main)

GlobalEventChannel.INSTANCE.selectMessage({
    "hello": "hello world",
    "test": lambda ev: ev.reply("test")
})

try:
    app.launch_blocking()
except KeyboardInterrupt:
    pass
