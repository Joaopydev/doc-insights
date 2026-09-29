from typing import Callable

from src.shared.infrastructure.dynamodb.client import DynamoDBClient

from src.chat.application.use_cases.create_conversation.create_conversation import CreateConversationUseCase
from src.chat.infrastructure.repositories.document_repository import DocumentRepository
from src.chat.infrastructure.repositories.chat_repository import ChatRepository


class CreateConversationComposer:

    @staticmethod
    def compose() -> Callable:

        db_client = DynamoDBClient()
        use_case = CreateConversationUseCase(
            chat_repository=ChatRepository(db_client),
            document_repository=DocumentRepository(db_client),
        )

        return use_case.execute
