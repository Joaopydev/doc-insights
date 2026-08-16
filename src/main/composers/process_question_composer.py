from typing import Awaitable

from src.chat.application.use_cases.question_processing.process_question import ProcessQuestionUseCase
from src.chat.infrastructure.repositories.chat_repository import ChatRepository

from src.shared.infrastructure.ai.client import OpenAIClient
from src.shared.infrastructure.ai.embedding_generator import EmbeddingGenerator
from src.shared.infrastructure.ai.response_generator import ResponseGenerator
from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.eventbridge.client import EventBridgeClient
from src.shared.infrastructure.repositories.vector_repository import VectorRepository


class ProcessQuestionComposer:

    @staticmethod
    def compose() -> Awaitable:
        ai_client = OpenAIClient()
        db_client = DynamoDBClient()

        response_generator = ResponseGenerator(ai_client)
        embedding_generator = EmbeddingGenerator(ai_client)
        chat_repository = ChatRepository(db_client)
        vector_repository = VectorRepository()
        event_publisher = EventBridgeClient()

        use_case = ProcessQuestionUseCase(
            chat_repository=chat_repository,
            response_generator=response_generator,
            embedding_generator=embedding_generator,
            event_publisher=event_publisher,
            vector_repository=vector_repository,
        )
        return use_case.execute
