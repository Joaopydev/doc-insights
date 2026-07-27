from typing import Awaitable

from src.processing.application.use_cases.index_document import IndexDocumentUseCase
from src.processing.infrastructure.chunking.recursive_chunk_generator import RecursiveChunkGenerator
from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository
from src.processing.infrastructure.repositories.vector_repository import VectorRepository

from src.shared.infrastructure.storage.s3 import S3Client
from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.ai.client import OpenAIClient
from src.shared.infrastructure.ai.embedding_generator import EmbeddingGenerator


class IndexDocumentComposer:

    @staticmethod
    def compose() -> Awaitable:
        vector_repository = VectorRepository()
        repository = DocumentProcessingRepository(DynamoDBClient())
        chunk_generator = RecursiveChunkGenerator()
        embedding_generator = EmbeddingGenerator(OpenAIClient())
        storage_port = S3Client()

        use_case = IndexDocumentUseCase(
            repository=repository,
            vector_repository=vector_repository,
            chunk_generator=chunk_generator,
            embedding_generator=embedding_generator,
            storage_port=storage_port,
        )

        return use_case.execute
