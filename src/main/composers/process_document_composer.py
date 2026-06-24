from typing import Callable

from src.processing.application.use_cases.process_document import ProcessDocumentUseCase
from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository
from src.processing.infrastructure.extractors.text_extractor import TextExtractor

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.storage.s3 import S3Client


class ProcessDocumentComposer:

    @staticmethod
    def compose() -> Callable:
        repo = DocumentProcessingRepository(DynamoDBClient())
        use_case = ProcessDocumentUseCase(
            document_processing_repository=repo,
            text_extractor=TextExtractor(),
            storage_port=S3Client(),
        )

        return use_case.execute
