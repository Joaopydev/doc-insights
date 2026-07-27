from typing import Callable

from src.chat.presentation.controllers.question_controller import QuestionController
from src.chat.application.use_cases.ask_question.ask_question import AskQuestionUseCase
from src.chat.infrastructure.repositories.chat_repository import ChatRepository
from src.chat.infrastructure.repositories.document_repository import DocumentRepository

from src.shared.infrastructure.eventbridge.client import EventBridgeClient
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class AskQuestionComposer:

    @staticmethod
    def compose() -> Callable:

        db_client = DynamoDBClient()
        chat_repository = ChatRepository(db_client)
        document_repository = DocumentRepository(db_client)
        event_publisher = EventBridgeClient()
        use_case = AskQuestionUseCase(
            chat_repository=chat_repository,
            document_repository=document_repository,
            event_publisher=event_publisher
        )
        controller = QuestionController(use_case)

        return controller.handle
