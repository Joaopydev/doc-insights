import pytest

from tests.integration.with_infra.processing.fakes.fake_textractor import FakeTextExtractor
from tests.integration.with_infra.processing.fakes.fake_chunk_generator import FakeChunkGenerator
from tests.integration.with_infra.processing.fakes.fake_embedding_generator import FakeEmbeddingGenerator
from tests.integration.with_infra.processing.fakes.fake_vector_repository import FakeVectorRepository


from src.processing.application.use_cases.textract_completed import TextractCompletedUseCase
from src.processing.application.use_cases.start_extraction_text import StartExtractionTextUseCase
from src.processing.application.use_cases.index_document import IndexDocumentUseCase
from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.storage.s3 import S3Client
from src.shared.infrastructure.eventbridge.client import EventBridgeClient



@pytest.fixture
def start_extraction_text_use_case() -> StartExtractionTextUseCase:
    db_client = DynamoDBClient()

    return StartExtractionTextUseCase(
        document_processing_repository=DocumentProcessingRepository(db_client),
        text_extractor=FakeTextExtractor(),
    )


@pytest.fixture
def textract_completed_use_case() -> TextractCompletedUseCase:
    db_client = DynamoDBClient()

    return TextractCompletedUseCase(
        document_processing_repository=DocumentProcessingRepository(db_client),
        text_extractor=FakeTextExtractor(),
        storage_port=S3Client()
    )


@pytest.fixture
def index_document_use_case() -> IndexDocumentUseCase:
    db_client = DynamoDBClient()

    return IndexDocumentUseCase(
        repository=DocumentProcessingRepository(db_client),
        vector_repository=FakeVectorRepository(),
        chunk_generator=FakeChunkGenerator(),
        embedding_generator=FakeEmbeddingGenerator(),
        storage_port=S3Client(),
        event_publisher=EventBridgeClient(),
    )
