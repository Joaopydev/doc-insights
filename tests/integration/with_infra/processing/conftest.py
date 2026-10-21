import pytest

from tests.integration.with_infra.processing.fakes import FakeTextExtractor
from src.processing.application.use_cases.textract_completed import TextractCompletedUseCase
from src.processing.application.use_cases.start_extraction_text import StartExtractionTextUseCase
from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.storage.s3 import S3Client



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
