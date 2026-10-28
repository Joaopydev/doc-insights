from typing import Callable

from src.chat.infrastructure.repositories.chat_repository import ChatRepository
from src.chat.infrastructure.repositories.document_repository import DocumentRepository
from src.chat.application.use_cases.delete_conversation.delete_conversation import DeleteConversationUseCase
from src.chat.presentation.controllers.delete_conversation_controller import DeleteConversationController

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.repositories.vector_repository import VectorRepository
from src.shared.infrastructure.storage.s3 import S3Client


class DeleteConversationComposer:

    @staticmethod
    def compose() -> Callable:
        db_client = DynamoDBClient()
        chat_repository = ChatRepository(db_client)
        document_repository = DocumentRepository(db_client)
        vector_repository = VectorRepository()
        storage = S3Client()
        use_case = DeleteConversationUseCase(
            chat_repository=chat_repository,
            document_repository=document_repository,
            vector_repository=vector_repository,
            storage_port=storage,
        )
        controller = DeleteConversationController(use_case)

        return controller.handle
