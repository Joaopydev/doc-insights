from abc import ABC, abstractmethod
from src.chat.domain.entities.connection import Connection


class ConnectionRepository(ABC):

    @abstractmethod
    def create_connection(self, connection: Connection) -> None:
        pass

    @abstractmethod
    def delete_connection(self, connection_id: str) -> None:
        pass

    @abstractmethod
    def get_connection_by_user_id(self, user_id: str) -> Connection:
        pass
