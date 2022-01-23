from abc import ABCMeta, abstractmethod


class ContactOrBot(object):
    """此为 [Contact] 与 [Bot] 的唯一公共接口
    """

    id: int
