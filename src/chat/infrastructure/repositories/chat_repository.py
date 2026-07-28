from typing import Optional

from src.chat.domain.entities.chat_message import ChatMessage
from src.chat.domain.entities.conversation import Conversation
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

    def get_message_by_id(self, message_id: str) -> Optional[ChatMessage]:
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
            conversation_id=item["conversation_id"],
            content=item["content"],
            message_type=item["message_type"],
            created_at=item["created_at"],
        )

    def save_conversation(self, conversation: Conversation) -> None:
        self.db_client.save(
            table_name=settings.conversation_table,
            item=conversation.to_dict()
        )

    def get_conversation_by_document_id(self, document_id: str) -> Optional[Conversation]:
        item = self.db_client.query(
            table_name=settings.conversation_table,
            index_name="document-id-index",
            key_name="document_id",
            key_value=document_id,
        )
        if not item:
            return None

        return Conversation.restore(
            conversation_id=item["id"],
            document_id=item["document_id"],
            user_id=item["user_id"],
            created_at=item["created_at"],
        )
