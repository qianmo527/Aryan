


from .user import User


class Stranger(User):

    from ..message.message_receipt import MessageReceipt
    def sendMessage(self, message) -> MessageReceipt["Stranger"]:
        pass

    def delete(self):
        pass

    def nudge(self):
        pass

    from .friend import Friend
    def asFriend(self) -> Friend:
        return self.bot.getFriendOrFail(self.id)

    def asFriendOrNone(self):
        return self.bot.getFriend(self.id)
