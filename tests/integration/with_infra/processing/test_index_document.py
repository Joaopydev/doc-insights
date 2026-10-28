import pytest

from tests.integration.with_infra.processing.factories import create_document

from src.upload.infrastructure.repositories.document_repository import DocumentRepository

from src.shared.domain.entities.document import DocumentStatus
from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.storage.s3 import S3Client


@pytest.mark.asyncio
async def test_index_document_happy_path(index_document_use_case):
    s3_client = S3Client()
    db_client = DynamoDBClient()

    repository = DocumentRepository(db_client)

    text_content = "dummy text/to generate/document chunks"
    new_document = create_document(
        "test-user-id",
        filename="test_document.pdf",
        content_type="application/pdf",
        document_status=DocumentStatus.EXTRACTED,
    )
    new_document.textract_job_id = f"fake-textract-job-id/{new_document.id}"

    repository.insert_document(new_document)
    s3_client.put_object(
        key=new_document.extracted_text_key.get_value(),
        body=text_content.encode("utf-8"),
        content_type="text/plain",
    )

    await index_document_use_case.execute(new_document.extracted_text_key.get_value())

    document = repository.get_document_by_id(new_document.id)
    assert document.status == DocumentStatus.READY
