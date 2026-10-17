import requests

from src.upload.application.use_cases.create.create_document_dto import (
    CreateDocumentInput,
    DocumentMetadataInput,
)
from src.main.config.settings import settings


def test_create_document(create_document_use_case):

    pdf_content = b"%PDF-1.4 fake document data"
    file_metadata = DocumentMetadataInput(
        filename="documento_via_url.pdf",
        content_type="application/pdf",
    )
    input_data = CreateDocumentInput(
        user_id="test-user-id",
        metadata=file_metadata,

    )
    output = create_document_use_case.execute(input_data)

    assert "localhost:4566" in output.presigned_url
    assert settings.bucket_name in output.presigned_url

    http_response = requests.put(
        url=output.presigned_url,
        data=pdf_content,
        headers={"Content-Type": file_metadata.content_type},
        timeout=5,
    )

    assert http_response.status_code == 200

    s3_object = create_document_use_case.storage_port.read_object_content(output.document.s3_key.get_value())

    assert s3_object == pdf_content
