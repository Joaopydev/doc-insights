import pytest

from src.upload.application.use_cases.create.create_document import CreateDocumentUseCase
from src.upload.infrastructure.repositories.document_repository import DocumentRepository

from src.shared.infrastructure.storage.s3 import S3Client
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


@pytest.fixture
def create_document_use_case() -> CreateDocumentUseCase:

    s3_client = S3Client()
    document_repository = DocumentRepository(DynamoDBClient())
    return CreateDocumentUseCase(
        document_repository=document_repository,
        storage_port=s3_client,
    )
