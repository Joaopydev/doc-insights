from src.chat.domain.entities.chat_message import ChatMessage
from src.chat.application.ports.chat_repository import (
    ChatRepository as ChatRepositoryInterface
)

from src.shared.application.ports.db_client import DBClient
from src.main.config.settings import settings


class ChatRepository(ChatRepositoryInterface):

    def __init__(
        self,
        db_client: DBClient,
    ) -> None:

        self.db_client = db_client

    def save_message(self, chat_message: ChatMessage):
        self.db_client.save(
            table_name=settings.chat_table,
            item=chat_message.to_dict()
        )
