from abc import ABC, abstractmethod
from typing import Optional, List

from src.chat.domain.entities.chat_message import ChatMessage
from src.chat.domain.entities.conversation import Conversation


class ChatRepository(ABC):

    @abstractmethod
    def save_message(self, chat_message: ChatMessage) -> None:
        pass

    @abstractmethod
    def get_message_by_id(self, message_id: str) -> Optional[ChatMessage]:
        pass

    @abstractmethod
    def save_conversation(self, conversation: Conversation) -> None:
        pass

    @abstractmethod
    def get_conversation_by_document_id(self, document_id: str) -> Optional[Conversation]:
        pass

    @abstractmethod
    def get_messages(self, conversation_id: str) -> List[ChatMessage]:
        pass

    @abstractmethod
    def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        pass
