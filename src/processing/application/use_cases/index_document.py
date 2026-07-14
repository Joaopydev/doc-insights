from src.processing.application.ports.chunk_generator import ChunkGenerator
from src.processing.application.ports.embedding_generator import EmbeddingGenerator
from src.processing.application.ports.document_processing_repository import DocumentProcessingRepository

from src.shared.domain.value_objects.document_status import DocumentStatus
from src.shared.application.ports.storage_port import StoragePort


class IndexDocumentUseCase:

    def __init__(
        self,
        repository: DocumentProcessingRepository,
        chunk_generator: ChunkGenerator,
        embedding_generator: EmbeddingGenerator,
        storage_port: StoragePort,
    ):
        self.repository = repository
        self.chunk_generator = chunk_generator
        self.embedding_generator = embedding_generator
        self.storage_port = storage_port

    async def execute(self, extracted_text_key: str) -> None:
        document = self.repository.get_document_by_extracted_text_key(extracted_text_key)
        if not document:
            return

        if document.status != DocumentStatus.EXTRACTED:
            return

        self.repository.update_status(
            document_id=document.id,
            status=DocumentStatus.INDEXING
        )

        # RAG Workflow: Read the extracted text from S3, generate chunks, and create embeddings
        extracted_text = self.storage_port.read_object_content(document.extracted_text_key.get_value())
        chunks = self.chunk_generator.generate_chunks(extracted_text.decode("utf-8"))
        embeddings = await self.embedding_generator.generate_embedding(chunks)

        print(f"Chunks: {chunks}, Size: {len(chunks)}")
        print(f"Embeddings: {embeddings}, Size: {len(embeddings)}")
