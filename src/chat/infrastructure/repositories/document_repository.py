from typing import Optional

from src.chat.application.ports.document_repository import (
    DocumentRepository as DocumentRepositoryInterface
)
from src.shared.application.ports.db_client import DBClient
from src.shared.domain.entities.document import Document
from src.main.config.settings import settings

class DocumentRepository(DocumentRepositoryInterface):

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def get_document_by_id(self, document_id: str) -> Optional[Document]:
        item = self.db_client.get_item(
            table_name=settings.document_table,
            key={
                "id": document_id
            }
        )
        if not item:
            return None

        return Document.restore(
            document_id=item["id"],
            user_id=item["user_id"],
            s3_key=item["s3_key"],
            extracted_text_key=item["extracted_text_key"],
            metadata=item["metadata"],
            status=item["status"],
            created_at=item["created_at"],
            updated_at=item["updated_at"],
        )
