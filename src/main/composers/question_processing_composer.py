from typing import Awaitable

from src.chat.application.use_cases.question_processing.question_processing_started import QuestionProcessingUseCase
from src.chat.infrastructure.repositories.chat_repository import ChatRepository

from src.processing.infrastructure.repositories.vector_repository import VectorRepository
from src.shared.infrastructure.ai.embedding_generator import EmbeddingGenerator
from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.ai.client import OpenAIClient


class QuestionProcessingComposer:

    @staticmethod
    def compose() -> Awaitable:

        chat_repository = ChatRepository(DynamoDBClient())
        vector_repository = VectorRepository()
        embedding_generator = EmbeddingGenerator(OpenAIClient())

        use_case = QuestionProcessingUseCase(
            chat_repository=chat_repository,
            vector_repository=vector_repository,
            embedding_generator=embedding_generator,
        )

        return use_case.execute
