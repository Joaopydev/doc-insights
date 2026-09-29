from pydantic import BaseModel

from src.shared.domain.entities.document import Document


class GetDocumentByIdInput(BaseModel):
    user_id: str
    document_id: str


class GetDocumentByIdOutput(BaseModel):
    document: Document
