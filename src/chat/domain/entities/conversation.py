from dataclasses import dataclass
from datetime import datetime, UTC
from typing import Dict
from uuid import uuid4


@dataclass
class Conversation:
    id: str
    document_id: str
    user_id: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        document_id: str,
        user_id: str,
    ) -> "Conversation":
        conversation_id = str(uuid4())
        created_at = datetime.now(UTC)

        return cls(
            id=conversation_id,
            document_id=document_id,
            user_id=user_id,
            created_at=created_at,
        )

    @classmethod
    def restore(
        cls,
        conversation_id: str,
        document_id: str,
        user_id: str,
        created_at: datetime,
    ) -> "Conversation":

        return cls(
            id=conversation_id,
            document_id=document_id,
            user_id=user_id,
            created_at=created_at,
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": self.id,
            "document_id": self.document_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
        }
