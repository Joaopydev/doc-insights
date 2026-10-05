from typing import Callable

from src.chat.presentation.controllers.list_user_conversations_controller import ListUserConversationsController
from src.chat.application.use_cases.list_conversations.list_user_conversations import ListUserConversationsUseCase
from src.chat.infrastructure.repositories.chat_repository import ChatRepository

from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class ListUserConversationsComposer:

    @staticmethod
    def compose() -> Callable:
        repository = ChatRepository(DynamoDBClient())
        use_case = ListUserConversationsUseCase(chat_repository=repository)
        controller = ListUserConversationsController(use_case=use_case)

        return controller.handle
