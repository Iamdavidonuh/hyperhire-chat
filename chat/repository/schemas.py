from dataclasses import dataclass, asdict
from chat.models import Message


@dataclass
class MessageSchema:
    message_type: Message.MessageType
    sender: str
    text: str | None = None
    media: str | None = None

    def to_dict(self) -> dict:
        asdict(self)
