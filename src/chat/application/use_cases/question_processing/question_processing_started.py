from src.chat.application.events.question_asked_event import QuestionAskedEvent
from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.domain.entities.chat_message import ChatMessage
from src.chat.domain.value_objects.message_type import MessageType
from src.chat.application.events.question_answered_event import QuestionAnsweredEvent
from src.chat.application.ports.response_cache import ResponseCache

from src.shared.application.ports.event_publisher import EventPublisher
from src.shared.application.ports.message_publisher import MessagePublisher


class QuestionProcessingUseCase:

    def __init__(
        self,
        chat_repository: ChatRepository,
        event_publisher: EventPublisher,
        response_cache: ResponseCache,
        message_publisher: MessagePublisher
    ):
        self.chat_repository = chat_repository
        self.event_publisher = event_publisher
        self.response_cache = response_cache
        self.message_publisher = message_publisher

    async def execute(self, event: QuestionAskedEvent):

        print("Before Dynamodb Connected")
        message = self.chat_repository.get_message_by_id(event.message_id)
        if not message:
            return
        print("After Dynamodb Connected")

        print("Befero Redis")
        cache_key = self.response_cache.create_cache_key(
            document_id=event.document_id,
            question=message.content,
        )
        cached_response = self.response_cache.get(cache_key)
        print("After Redis")

        if not cached_response:
            print("Before SQS")
            self.message_publisher.send_message(
                {
                    "message_id": message.id,
                    "document_id": event.document_id,
                    "cache_key": cache_key,
                }
            )
            print("After SQS")
            return

        ai_message = ChatMessage.create(
            conversation_id=message.conversation_id,
            content=cached_response,
            message_type=MessageType.ANSWER,
        )
        self.chat_repository.save_message(ai_message)

        self.event_publisher.publish(
            QuestionAnsweredEvent(
                conversation_id=message.conversation_id
            )
        )
