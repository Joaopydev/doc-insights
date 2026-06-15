from src.upload.application.ports.document_repository import (
    DocumentRepository as DocumentRepositoryInterface
)
from src.upload.domain.entities.document import Document
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
