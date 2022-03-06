from .contact import Contact
from .user_or_bot import UserOrBot


class User(Contact, UserOrBot):
    id: int
    remark: str = None

    @property
    def remarkOrNick(self):
        """获取非空备注或昵称.

        若 [备注][User.remark] 不为空则返回备注, 为空则返回 [User.nick]
        """
        return self.remark or self.nickname

    @property
    def remarkOrNameCard(self):
        """获取非空备注或群名片.

        若 [备注][User.remark] 不为空则返回备注, 为空则返回 [Member.nameCard]
        """
        pass

    @property
    def remarkOrNameCardOrNick(self):
        """获取非空备注或群名片或昵称.

        若 [备注][User.remark] 不为空则返回备注, 为空则返回 [Member.nameCardOrNick]
        """

    def sendMessage(self):
        pass

    def nudge(self):
        pass

    def queryProfile(self):
        """查询用户信息"""
        pass
