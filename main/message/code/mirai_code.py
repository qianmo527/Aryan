from abc import ABCMeta, abstractmethod


class MiraiCode(object):

    @classmethod
    def __new__(cls: type["MiraiCode"], *args, **kwargs) -> "MiraiCode":
        raise
        return super().__new__(cls)

    @staticmethod
    def deserializeMiraiCode(content: str): pass
