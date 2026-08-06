from datetime import datetime, UTC
from dataclasses import dataclass

@dataclass(frozen=True)
class Connection:
    id: str
    user_id: str
    created_at: datetime

    @classmethod
    def create(cls, connection_id: str, user_id: str) -> "Connection":
        return cls(id=connection_id, user_id=user_id, created_at=datetime.now(UTC))

    @classmethod
    def restore(cls, connection_id: str, user_id: str, created_at: datetime) -> "Connection":
        return cls(id=connection_id, user_id=user_id, created_at=created_at)

    def to_dict(self) -> dict:
        return {
            "connection_id": self.id,
            "user_id": self.user_id,
            "created_at": self.created_at
        }
