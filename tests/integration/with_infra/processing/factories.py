from typing import Optional

from src.shared.domain.entities.document import (
    Document,
    DocumentStatus,
)


def create_document(
    user_id: str,
    filename: str,
    content_type: str,
    document_status: Optional[DocumentStatus] = None
) -> Document:
    document = Document.create(
        user_id=user_id,
        metadata={
            "filename": filename,
            "content_type": content_type,
        }
    )
    if document_status:
        document.status = document_status

    return document
