from pydantic import BaseModel


from .message import Message


class SingleMessage(Message):
    """单个消息元素 与之相对的是 [MessageChain] 是多个 [SingleMessage] 的集合
    """
    ...

class MessageMetadata(SingleMessage):
    """返回空字符串
    """

    def contentToString(self) -> str:
        return str()

class MessageContent(SingleMessage):
    """带内容的消息 [纯文本 At 特殊信息 图片 富文本 服务消息 原生表情 合并转发 语音 商城表情 音乐分享]
    """
    ...
