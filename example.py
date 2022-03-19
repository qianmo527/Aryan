import asyncio
from typing import Union

from src.aryan import Mirai, MiraiSession, Bot, BotConfiguration
from src.aryan import GlobalEventChannel, EventPriority, ConcurrencyKind, ListeningStatus
from src.aryan import GroupMessage, FriendMessage, LaunchEvent
from src.aryan import Plain, Face
from src.aryan import ListenerHostInterface


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


# @GlobalEventChannel.INSTANCE.trigger()
def main(event: Union[GroupMessage, FriendMessage]):
    print("listener received event:", event.__class__.__name__)
    return event.reply(event.__class__.__name__)

    event.intercept()

    # next_event: FriendMessage = await event.bot.eventChannel.nextEvent(FriendMessage)
    # await next_event.reply("True")

# GlobalEventChannel.INSTANCE.subscribeOnce(handler=main)


# GlobalEventChannel.INSTANCE.subscribeMessages({
#     "签到": "签到成功!!!",
#     "test": Plain("received"),
#     "hello world": [Plain("这是联合消息"), Face(176)],
#     "test2": lambda ev: ev.reply("test"),
#     "default": "default reply"
# }, default=True)


# @GlobalEventChannel.addBackgroundTask()
# async def backgroundTask():
#     while True:
#         print("in backgroup task")
#         await asyncio.sleep(1)


class ListenerHost(ListenerHostInterface):

    @ListenerHostInterface.EventHandler
    async def onEvent(self, event: Union[GroupMessage, FriendMessage]) -> ListeningStatus.STOPPED:
        print("Message received")
        return ListeningStatus.LISTENING

    @ListenerHostInterface.EventHandler
    def quick_response(self, event: GroupMessage) -> ListeningStatus.STOPPED:
        return event.reply("hello world!!!")

GlobalEventChannel.INSTANCE.registerListenerHost(ListenerHost())


try:
    app.launch_blocking()
except KeyboardInterrupt:
    pass
