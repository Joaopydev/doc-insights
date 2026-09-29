from typing import Callable

from src.upload.presentation.controllers.get_document_by_id_controller import GetDocumentByIdController
from src.upload.application.use_cases.get.get_document_by_id import GetDocumentByIdUseCase
from src.upload.infrastructure.repositories.document_repository import DocumentRepository

from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class GetDocumentByIdComposer:

    @staticmethod
    def compose() -> Callable:
        repository = DocumentRepository(DynamoDBClient())
        use_case = GetDocumentByIdUseCase(repository)
        controller = GetDocumentByIdController(use_case)

        return controller.handle
