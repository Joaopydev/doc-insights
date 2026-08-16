from typing import Awaitable

from src.chat.application.use_cases.question_processing.question_processing_started import QuestionProcessingUseCase
from src.chat.infrastructure.repositories.chat_repository import ChatRepository
from src.chat.infrastructure.cache.redis_response_cache import RedisResponseCache

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.eventbridge.client import EventBridgeClient
from src.shared.infrastructure.sqs.sqs_publisher import SQSPublisher


class QuestionProcessingComposer:

    @staticmethod
    def compose() -> Awaitable:

        chat_repository = ChatRepository(DynamoDBClient())
        event_publisher = EventBridgeClient()
        response_cache = RedisResponseCache()
        message_publisher = SQSPublisher()

        use_case = QuestionProcessingUseCase(
            chat_repository=chat_repository,
            event_publisher=event_publisher,
            response_cache=response_cache,
            message_publisher=message_publisher,
        )

        return use_case.execute
