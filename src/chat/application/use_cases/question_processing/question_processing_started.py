from src.chat.application.events.question_asked_event import QuestionAskedEvent
from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.application.services.context_builder import ContextBuilder
from src.chat.domain.entities.chat_message import ChatMessage
from src.chat.domain.value_objects.message_type import MessageType
from src.chat.application.events.question_answered_event import QuestionAnsweredEvent

from src.shared.application.ports.response_generator import ResponseGenerator
from src.shared.application.ports.embedding_generator import EmbeddingGenerator
from src.shared.application.ports.event_publisher import EventPublisher
from src.shared.application.ports.vector_repository import VectorRepository


class QuestionProcessingUseCase:

    def __init__(
        self,
        chat_repository: ChatRepository,
        vector_repository: VectorRepository,
        embedding_generator: EmbeddingGenerator,
        response_generator: ResponseGenerator,
        event_publisher: EventPublisher,
    ):
        self.chat_repository = chat_repository
        self.vector_repository = vector_repository
        self.embedding_generator = embedding_generator
        self.response_generator = response_generator
        self.event_publisher = event_publisher

    async def execute(self, event: QuestionAskedEvent):
        message = self.chat_repository.get_message_by_id(event.message_id)
        if not message:
            return

        message_embedding = await self.embedding_generator.generate_embedding([message.content])
        chunks = self.vector_repository.semantic_similarity_search(
            embedding=message_embedding[0],
            document_id=event.document_id,
        )
        context = ContextBuilder.build(chunks)
        response = await self.response_generator.generate(
            question=message.content,
            context=context,
        )
        ai_message = ChatMessage.create(
            conversation_id=message.conversation_id,
            content=response,
            message_type=MessageType.ANSWER,
        )
        self.chat_repository.save_message(ai_message)

        self.event_publisher.publish(
            QuestionAnsweredEvent(
                conversation_id=message.conversation_id
            )
        )
