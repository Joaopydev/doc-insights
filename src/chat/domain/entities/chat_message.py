from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Dict
from uuid import uuid4


@dataclass
class ChatMessage:
    id: str
    document_id: str
    conversation_id: str
    user_id: str
    message: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        document_id: str,
        conversation_id: str,
        user_id: str,
        message: str,
    ) -> "ChatMessage":
        message_id = str(uuid4())
        created_at = datetime.now(UTC)

        return cls(
            id=message_id,
            document_id=document_id,
            conversation_id=conversation_id,
            user_id=user_id,
            message=message,
            created_at=created_at,
        )

    @classmethod
    def restore(
        cls,
        message_id: str,
        document_id: str,
        conversation_id: str,
        user_id: str,
        message: str,
        created_at: datetime,
    ) -> "ChatMessage":

        return cls(
            id=message_id,
            document_id=document_id,
            conversation_id=conversation_id,
            user_id=user_id,
            message=message,
            created_at=created_at,
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "document_id": self.document_id,
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "message": self.message,
            "created_at": self.created_at,
        }
