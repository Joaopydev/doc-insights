from typing import Callable

from src.processing.application.use_cases.process_document import ProcessDocumentUseCase
from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class ProcessDocumentComposer:

    @staticmethod
    def compose() -> Callable:
        repo = DocumentProcessingRepository(DynamoDBClient())
        use_case = ProcessDocumentUseCase(repo)

        return use_case.execute
