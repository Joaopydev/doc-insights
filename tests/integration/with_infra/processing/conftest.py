import pytest

from tests.integration.with_infra.processing.fakes import FakeTextExtractor
from src.processing.application.use_cases.start_extraction_text import StartExtractionTextUseCase
from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository

from src.shared.infrastructure.dynamodb.client import DynamoDBClient


@pytest.fixture
def start_extraction_text_use_case() -> StartExtractionTextUseCase:
    db_client = DynamoDBClient()

    return StartExtractionTextUseCase(
        document_processing_repository=DocumentProcessingRepository(db_client),
        text_extractor=FakeTextExtractor(),
    )
