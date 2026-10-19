from tests.integration.with_infra.processing.factories import create_document

from src.upload.infrastructure.repositories.document_repository import DocumentRepository

from src.shared.domain.entities.document import DocumentStatus
from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.storage.s3 import S3Client


def test_start_extraction_text_happy_path(start_extraction_text_use_case):
    s3_client = S3Client()
    db_client = DynamoDBClient()

    repository = DocumentRepository(db_client)

    pdf_content = b"%PDF-1.4 fake document data"
    new_document = create_document(
        "test-user-id",
        filename="test_document.pdf",
        content_type="application/pdf"
    )

    repository.insert_document(new_document)
    s3_client.put_object(
        key=new_document.s3_key.get_value(),
        body=pdf_content,
        content_type=new_document.metadata.content_type,
    )

    start_extraction_text_use_case.execute(new_document.s3_key.get_value())

    recovered_document = repository.get_document_by_id(new_document.id)

    assert recovered_document.status == DocumentStatus.EXTRACTING
    assert recovered_document.textract_job_id
