from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Dict
from uuid import uuid4


@dataclass
class ChatMessage:
    id: str
    conversation_id: str
    content: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        conversation_id: str,
        content: str,
    ) -> "ChatMessage":
        message_id = str(uuid4())
        created_at = datetime.now(UTC)

        return cls(
            id=message_id,
            conversation_id=conversation_id,
            content=content,
            created_at=created_at,
        )

    @classmethod
    def restore(
        cls,
        message_id: str,
        conversation_id: str,
        content: str,
        created_at: datetime,
    ) -> "ChatMessage":

        return cls(
            id=message_id,
            conversation_id=conversation_id,
            content=content,
            created_at=created_at,
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
        }
