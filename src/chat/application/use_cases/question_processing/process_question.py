from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.application.services.context_builder import ContextBuilder
from src.chat.domain.entities.chat_message import ChatMessage
from src.chat.domain.value_objects.message_type import MessageType
from src.chat.application.use_cases.question_processing.process_question_dto import ProcessQuestionInput
from src.chat.application.events.question_answered_event import QuestionAnsweredEvent
from src.chat.application.events.update_cache_event import UpdateCacheEvent

from src.shared.application.ports.response_generator import ResponseGenerator
from src.shared.application.ports.embedding_generator import EmbeddingGenerator
from src.shared.application.ports.event_publisher import EventPublisher
from src.shared.application.ports.vector_repository import VectorRepository


class ProcessQuestionUseCase:

    def __init__(
        self,
        chat_repository: ChatRepository,
        response_generator: ResponseGenerator,
        embedding_generator: EmbeddingGenerator,
        event_publisher: EventPublisher,
        vector_repository: VectorRepository,
    ) -> None:

        self.chat_repository = chat_repository
        self.response_generator = response_generator
        self.embedding_generator = embedding_generator
        self.event_publisher = event_publisher
        self.vector_repository = vector_repository

    async def execute(self, input_dto: ProcessQuestionInput) -> None:

        message = self.chat_repository.get_message_by_id(input_dto.message_id)
        if not message:
            return

        message_embedding = await self.embedding_generator.generate_embedding([message.content])
        chunks = self.vector_repository.semantic_similarity_search(
            embedding=message_embedding[0],
            document_id=input_dto.document_id,
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
        self.event_publisher.publish(
            UpdateCacheEvent(
                cache_key=input_dto.cache_key,
                generated_response=response,
            )
        )
