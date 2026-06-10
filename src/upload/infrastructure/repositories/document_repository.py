from src.shared.infrastructure.dynamodb.tables import DocumentTable
from src.upload.application.ports.document_repository import (
    DocumentRepository as DocumentRepositoryInterface
)
from src.upload.domain.entities.document import Document
from src.shared.application.ports.db_client import DBClient


class DocumentRepository(DocumentRepositoryInterface):

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def save(self, document: Document):
        self.db_client.save(
            table_name=DocumentTable.TABLE_NAME,
            item=document.to_dict()
        )
