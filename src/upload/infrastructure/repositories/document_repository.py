from src.shared.infrastructure.dynamodb.tables import DocumentTable
from src.upload.application.ports.document_repository import (
    DocumentRepository as DocumentRepositoryInterface
)
from src.upload.domain.entities.document import Document
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class DocumentRepository(DocumentRepositoryInterface):

    def __init__(self, dynamodb_client: DynamoDBClient):
        self.dynamodb_client = dynamodb_client

    def save(self, document: Document):
        self.dynamodb_client.put_item(
            table_name=DocumentTable.TABLE_NAME,
            item=document.to_dict()
        )
