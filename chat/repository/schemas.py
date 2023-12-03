from dataclasses import dataclass, asdict
from chat.models import Message


@dataclass
class MessageSchema:
    message_type: Message.MessageType
    room: str
    sender: str | None = None
    text: str | None = None
    media: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)
