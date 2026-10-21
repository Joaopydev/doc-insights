from tests.integration.with_infra.processing.factories import create_document

from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository
from src.upload.infrastructure.repositories.document_repository import DocumentRepository

from src.shared.domain.entities.document import DocumentStatus
from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.storage.s3 import S3Client


def test_textract_completed_happy_path(textract_completed_use_case):

    storage = S3Client()
    db_client = DynamoDBClient()
    repository = DocumentProcessingRepository(db_client)
    storage_repository = DocumentRepository(db_client)

    document = create_document(
        user_id="test-user-id",
        filename="test_document.pdf",
        content_type="application/pdf",
        document_status=DocumentStatus.EXTRACTING,
    )
    document.textract_job_id = f"fake-textract-job-id/{document.id}"

    storage_repository.insert_document(document)

    textract_completed_use_case.execute(document.textract_job_id)

    s3_object = storage.read_object_content(document.extracted_text_key.get_value())
    recovered_document = repository.get_document_by_textract_job_id(document.textract_job_id)

    assert s3_object.decode("utf-8") == document.textract_job_id
    assert recovered_document.status == DocumentStatus.EXTRACTED
