from typing import Optional

from src.chat.application.ports.connection_repository import (
    ConnectionRepository as ConnectionRepositoryInterface
)
from src.chat.domain.entities.connection import Connection

from src.shared.application.ports.db_client import DBClient
from src.main.config.settings import settings


class ConnectionRepository(ConnectionRepositoryInterface):

    def __init__(self, db_client: DBClient) -> None:
        self.db_client = db_client

    def create_connection(self, connection: Connection) -> None:
        self.db_client.save(
            table_name=settings.connections_table,
            item=connection.to_dict()
        )

    def delete_connection(self, connection_id: str) -> None:
        self.db_client.delete_item(
            table_name=settings.connections_table,
            key={
                "connection_id": {"S": connection_id}
            }
        )

    def get_connection_by_user_id(self, user_id: str) -> Optional[Connection]:
        item = self.db_client.query(
            table_name=settings.connections_table,
            index_name="user-id-index",
            key_name="user_id",
            key_value=user_id,
        )
        if not item:
            return None

        return Connection.restore(
            connection_id=item["connection_id"],
            user_id=item["user_id"],
            created_at=item["created_at"]
        )
