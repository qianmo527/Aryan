# Aryan

## 简介
简单介绍一下本项目有何有点以及为何值得使用  
* 本项目~~写的很烂~~源码通俗易懂 方便阅读与使用
* 作者（也就是我）单纯 善良 可爱 迷人 友善...（省略一万字）

## 安装
``pip install aryan``  
或使用包管理工具poetry  
``poetry add aryan``

## 部署
### 配置mirai-api-http（mah）
本项目要求使用mah v2.0 并开启http与websocket（别问 问就是我懒

### 配置你的python文件
```python
import asyncio
from aryan import Mirai, MiraiSession, BotConfiguration, Bot
from aryan import GroupMessage, GlobalEventChannel

app = Mirai(
    MiraiSession(
        verify_key="verifyKey",
        host="localhost:8080",
    ),
    loop=asyncio.get_event_loop(),
    bots=[
        Bot(BotConfiguration(account=...)),
        Bot(BotConfiguration(account=...))
    ]
)

async def main(event: GroupMessage):
    print("received event:", type(event))

GlobalEventChannel.INSTANCE.subscribeAlways(GroupMessage, main)

app.launch_blocking()
```

如果在使用本项目中遇到任何问题，请不要生气，不要砸电脑，可以友好的提个issue或者加入qq交流群~~喷项目~~交流

[qq交流群](https://jq.qq.com/?_wv=1027&k=BUU9hkkN)
