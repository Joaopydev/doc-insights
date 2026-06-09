from dataclasses import dataclass

from src.upload.domain.entities.document import Document


@dataclass(frozen=True)
class CreateDocumentOutput:
    document: Document
    presigned_url: str
