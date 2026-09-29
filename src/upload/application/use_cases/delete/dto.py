from pydantic import BaseModel


class DeleteDocumentInput(BaseModel):
    user_id: str
    document_id: str
