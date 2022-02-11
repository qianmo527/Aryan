from pydantic import BaseModel, BaseConfig
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from ..bot import Bot


class ContactOrBot(BaseModel, object):
    """此为 [Contact] 与 [Bot] 的唯一公共接口
    """

    id: int
    bot: "Bot" = None

    @property
    def avatarUrl(self) -> str:
        return f"http://q1.qlogo.cn/g?b=qq&nk={self.id}&s=640"

    class Config(BaseConfig):
        json_encoders = {
            datetime: lambda v: v.timestamp()
        }
        arbitrary_types_allowed = True

    def __repr__(self) -> str:
        return self.__class__.__name__ + "(" + ", ".join(
            (
               f"{k}={repr(v)}"
                for k, v in self.__dict__.items() if k != "type" and v 
            )
        ) + ")"
