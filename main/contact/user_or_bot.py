from .contact_or_bot import ContactOrBot


class UserOrBot(ContactOrBot):
    nickname: str = None # 获取昵称  TODO

    def nudge(self):
        """Nudge.sendTo() 发送这个戳一戳消息"""
        pass
