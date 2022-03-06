from datetime import datetime


from .single_message import MessageMetadata


class Source(MessageMetadata):
    type: str = "Source"
    id: int
    time: datetime

    def __repr__(self) -> str:
        return f"Source({self.id}, time={self.time})"

    def __str__(self) -> str:
        return f"Source({self.id}, time={self.time})"
