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

    def get_message_by_id(self, message_id: str) -> ChatMessage:
        item = self.db_client.get_item(
            table_name=settings.chat_table,
            key={
                "id": message_id
            }
        )
        if not item:
            return None

        return ChatMessage.restore(
            message_id=item["id"],
            document_id=item["document_id"],
            conversation_id=item["conversation_id"],
            user_id=item["user_id"],
            content=item["content"],
            created_at=item["created_at"],
        )
