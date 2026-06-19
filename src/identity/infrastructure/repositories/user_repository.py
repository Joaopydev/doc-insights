from src.identity.application.ports.user_repository import (
    UserRepository as UserRepositoryInterface
)
from src.shared.application.ports.db_client import DBClient
from src.identity.domain.entities.user import UserIdentity
from src.main.config.settings import settings


class UserRepository(UserRepositoryInterface):

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def insert_user(self, user: UserIdentity):
        self.db_client.save(
            table_name=settings.user_table,
            item=user.to_dict(),
        )

    def get_by_id(self, user_id: str) -> UserIdentity:
        item = self.db_client.get_item(
            table_name=settings.user_table,
            key={
                "id": user_id
            }
        )
        if not item:
            return None

        return UserIdentity(**item)

    def get_by_email(self, email: str) -> UserIdentity:
        item = self.db_client.query(
            table_name=settings.user_table,
            index_name="email-index",
            key_name="email",
            key_value=email,
        )
        if not item:
            return None

        return UserIdentity(**item)
