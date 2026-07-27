from src.chat.application.events.question_asked_event import QuestionAskedEvent
from src.chat.application.ports.chat_repository import ChatRepository

from src.shared.application.ports.embedding_generator import EmbeddingGenerator
from src.processing.application.ports.vector_repository import VectorRepository


class QuestionProcessingUseCase:

    def __init__(
        self,
        chat_repository: ChatRepository,
        vector_repository: VectorRepository,
        embedding_generator: EmbeddingGenerator,
    ):
        self.chat_repository = chat_repository
        self.vector_repository = vector_repository
        self.embedding_generator = embedding_generator

    async def execute(self, event: QuestionAskedEvent):
        message = self.chat_repository.get_message_by_id(event.message_id)
        if not message:
            return

        message_embedding = await self.embedding_generator.generate_embedding([message.content])
        document_chunks = self.vector_repository.semantic_similarity_search(
            embedding=message_embedding[0],
            document_id=event.document_id,
        )

        print(f"Retrieval Chunks: {document_chunks}")
