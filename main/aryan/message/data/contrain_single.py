

from .single_message import SingleMessage


class ConstrainSingle(SingleMessage):
    """约束一个 [MessageChain] 中只存在这以一种类型的元素 新元素会替换旧元素 保持原顺序
    """

    key: MessageKey
