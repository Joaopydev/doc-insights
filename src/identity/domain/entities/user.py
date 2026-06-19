from datetime import datetime, UTC
from dataclasses import dataclass
from uuid import uuid4


@dataclass
class UserIdentity:
    id: str
    name: str
    email: str
    password: str
    created_at: datetime


    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def create(
        cls,
        name: str,
        email: str,
        password: str,
    ):
        user_id = str(uuid4())
        now = datetime.now(UTC)

        return cls(
            id=user_id,
            name=name,
            email=email,
            password=password,
            created_at=now
        )

    @classmethod
    def restore(
        cls,
        user_id: str,
        name: str,
        email: str,
        password: str,
        created_at: datetime,
    ):
        return cls(
            id=user_id,
            name=name,
            email=email,
            password=password,
            created_at=created_at
        )
