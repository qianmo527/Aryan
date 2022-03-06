from typing import TYPE_CHECKING, Union

from .contact_or_bot import ContactOrBot

if TYPE_CHECKING:
    from ..message.message_receipt import MessageReceipt
    from ..message.data.message import Message
    from ..message.data.plain import Plain


class Contact(ContactOrBot):
    id: int

    def sendMessage(self, message: Union["Message", str]) -> "MessageReceipt['Contact']":
        """发送消息

        Returns:
            MessageReceipt:  消息回折 可 [MessageReceipt.quote()] 或 [MessageReceipt.recall()]
        """

        message = message if isinstance(message, "Message") else Plain(message)

    def uploadImage(self, resource): pass

    def sendImage(self, image): pass

    def recallMessage(self, source): pass  # : Union[MessageChain, Source]
