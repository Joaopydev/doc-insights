from typing import Callable

from src.chat.presentation.controllers.question_controller import QuestionController
from src.chat.application.use_cases.ask_question.ask_question import AskQuestionUseCase
from src.chat.infrastructure.repositories.chat_repository import ChatRepository

from src.shared.infrastructure.eventbridge.client import EventBridgeClient
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class AskQuestionComposer:

    @staticmethod
    def compose() -> Callable:

        repo = ChatRepository(DynamoDBClient())
        event_publisher = EventBridgeClient()
        use_case = AskQuestionUseCase(
            chat_repository=repo,
            event_publisher=event_publisher
        )
        controller = QuestionController(use_case)

        return controller.handle
