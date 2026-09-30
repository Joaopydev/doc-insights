from src.upload.application.ports.document_repository import (
    DocumentRepository as DocumentRepositoryInterface
)
from src.shared.domain.entities.document import Document
from src.shared.application.ports.db_client import DBClient

from src.main.config.settings import settings


class DocumentRepository(DocumentRepositoryInterface):

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def insert_document(self, document: Document):
        self.db_client.save(
            table_name=settings.document_table,
            item=document.to_dict()
        )

    def get_document_by_id(self, document_id: str) -> Document:
        item = self.db_client.get_item(
            table_name=settings.document_table,
            key={
                "id": document_id,
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
            textract_job_id=item.get("textract_job_id"),
            conversation_id=item.get("conversation_id"),
        )

    def delete_document_by_id(self, document_id: str) -> None:
        self.db_client.delete_item(
            table_name=settings.document_table,
            key={
                "id": document_id,
            }
        )
