from typing import Callable

from src.chat.infrastructure.repositories.chat_repository import ChatRepository
from src.chat.application.use_cases.get_conversation.get_conversation_by_id import GetConversationByIdUseCase
from src.chat.presentation.controllers.get_conversation_by_id_controller import GetConversationByIdController

from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class GetConversationByIdComposer:

    @staticmethod
    def compose() -> Callable:
        repository = ChatRepository(DynamoDBClient())
        use_case = GetConversationByIdUseCase(repository)
        controller = GetConversationByIdController(use_case)

        return controller.handle
