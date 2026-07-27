from abc import ABC, abstractmethod

from src.chat.domain.entities.chat_message import ChatMessage


class ChatRepository(ABC):

    @abstractmethod
    def save_message(self, chat_message: ChatMessage) -> None:
        pass

    @abstractmethod
    def get_message_by_id(self, message_id: str) -> ChatMessage:
        pass
