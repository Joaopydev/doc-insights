from typing import Callable

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.storage.s3 import S3Client

from src.upload.infrastructure.repositories.document_repository import DocumentRepository
from src.upload.application.use_cases.create_document import CreateDocumentUseCase
from src.upload.presentation.controllers.create_document_controller import CreateDocumentController


class CreateDocumentComposer:

    @staticmethod
    def compose() -> Callable:
        db_client = DynamoDBClient()
        document_repository = DocumentRepository(db_client=db_client)
        use_case = CreateDocumentUseCase(
            document_repository=document_repository,
            storage_port=S3Client()
        )
        controller = CreateDocumentController(use_case=use_case)
        return controller.handle
