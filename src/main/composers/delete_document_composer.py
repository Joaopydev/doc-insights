from typing import Callable

from src.upload.presentation.controllers.delete_document_controller import DeleteDocumentController
from src.upload.application.use_cases.delete.delete_document import DeleteDocumentUseCase
from src.upload.infrastructure.repositories.document_repository import DocumentRepository

from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class DeleteDocumentComposer:

    @staticmethod
    def compose() -> Callable:
        repository = DocumentRepository(DynamoDBClient())
        use_case = DeleteDocumentUseCase(repository)
        controller = DeleteDocumentController(use_case)

        return controller.handle
