from typing import Awaitable

from src.chat.application.use_cases.question_processing.question_processing_started import QuestionProcessingUseCase
from src.chat.infrastructure.repositories.chat_repository import ChatRepository

from src.processing.infrastructure.repositories.vector_repository import VectorRepository
from src.shared.infrastructure.ai.embedding_generator import EmbeddingGenerator
from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.ai.client import OpenAIClient
from src.shared.infrastructure.ai.response_generator import ResponseGenerator
from src.shared.infrastructure.eventbridge.client import EventBridgeClient


class QuestionProcessingComposer:

    @staticmethod
    def compose() -> Awaitable:

        chat_repository = ChatRepository(DynamoDBClient())
        vector_repository = VectorRepository()
        ai_client = OpenAIClient()
        embedding_generator = EmbeddingGenerator(ai_client)
        response_generator = ResponseGenerator(ai_client)
        event_publisher = EventBridgeClient()

        use_case = QuestionProcessingUseCase(
            chat_repository=chat_repository,
            vector_repository=vector_repository,
            embedding_generator=embedding_generator,
            response_generator=response_generator,
            event_publisher=event_publisher,
        )

        return use_case.execute
