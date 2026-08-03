from typing import Callable

from src.chat.application.use_cases.get_messages.get_messages import GetMessagesUseCase
from src.chat.presentation.controllers.get_messages import GetMessagesController
from src.chat.infrastructure.repositories.chat_repository import ChatRepository

from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class GetMessagesComposer:

    @staticmethod
    def compose() -> Callable:

        chat_repository = ChatRepository(DynamoDBClient())
        use_case = GetMessagesUseCase(chat_repository)
        controller = GetMessagesController(use_case)

        return controller.handle
