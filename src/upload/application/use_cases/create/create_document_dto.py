from enum import Enum
from pydantic import BaseModel

from src.shared.domain.entities.document import Document

class ContentType(str, Enum):
    PDF = "application/pdf"
    # PNG = "image/png"
    # JPEG = "image/jpeg"
    # JPG = "image/jpg"

class DocumentMetadataInput(BaseModel):
    filename: str
    content_type: ContentType

class CreateDocumentInput(BaseModel):
    user_id: str
    metadata: DocumentMetadataInput

class CreateDocumentOutput(BaseModel):
    document: Document
    presigned_url: str
