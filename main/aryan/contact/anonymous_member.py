


from .member import Member


class AnonymousMember(Member):
    anonymousId: str

    def sendMessage(self, message):
        raise

    def uploadImage(self, resource):
        raise
