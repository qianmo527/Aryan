import asyncio
from typing import Union

from src.aryan import Mirai, MiraiSession, Bot, BotConfiguration
from src.aryan import GlobalEventChannel, EventPriority, ConcurrencyKind, ListeningStatus
from src.aryan import GroupMessage, FriendMessage, MessageEvent
from src.aryan import Plain, Face
from src.aryan import ListenerHostInterface


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
    # await event.reply(str(type(event)))

    event.intercept()

    # next_event: FriendMessage = await event.bot.eventChannel.nextEvent(FriendMessage)
    # await next_event.reply("True")

GlobalEventChannel.INSTANCE.subscribeOnce(GroupMessage, main)

GlobalEventChannel.INSTANCE.subscribeMessages({
    "签到.*?": "签到成功!!!",
    "test": Plain("received"),
    "hello world": [Plain("这是联合消息"), Face(176)],
    "test2": lambda ev: ev.reply("test"),
    "default": "default reply"
}, default=True)


class ListenerHost(ListenerHostInterface):
    ignore = ["ignored_function"]
    filter = [] or {}
    filter = [{}, lambda ev: ev.sender.id == 2816661524]  # TODO 是否支持动态更改(即是否list.copy())

    async def onEvent(event: Union[GroupMessage, FriendMessage]) -> ListeningStatus.STOPPED:
        print("Message received")

    def sync_quick_response(self):
        pass

    def tool(self):
        pass

    ignore.append(tool)

GlobalEventChannel.INSTANCE.registerListenerHost(ListenerHost())


try:
    app.launch_blocking()
except KeyboardInterrupt:
    pass
