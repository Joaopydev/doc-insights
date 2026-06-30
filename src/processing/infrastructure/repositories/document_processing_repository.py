from typing import Optional

from src.processing.application.ports.document_processing_repository import (
    DocumentProcessingRepository as DocumentProcessingRepositoryInterface
)
from src.shared.application.ports.db_client import DBClient
from src.shared.domain.entities.document import Document
from src.main.config.settings import settings

class DocumentProcessingRepository(DocumentProcessingRepositoryInterface):

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def get_document_by_storage_key(self, storage_key: str) -> Optional[Document]:
        item = self.db_client.query(
            table_name=settings.document_table,
            index_name="storage-key-index",
            key_name="s3_key",
            key_value=storage_key,
        )
        if not item:
            return None

        return Document.restore(**item)

    def update_status(self, document_id: str, status: str):
        self.db_client.update_item(
            table_name=settings.document_table,
            key={
                "id": document_id
            },
            update_expression="SET #status = :status",
            expression_attribute_names={
                "#status": "status"
            },
            expression_attribute_values={
                ":status": status
            }
        )

    def update_textract_job_id(self, document_id: str, job_id: str):
        self.db_client.update_item(
            table_name=settings.document_table,
            key={
                "id": document_id
            },
            update_expression="SET #textract_job_id = :textract_job_id",
            expression_attribute_names={
                "#textract_job_id": "textract_job_id"
            },
            expression_attribute_values={
                ":textract_job_id": job_id
            }
        )
