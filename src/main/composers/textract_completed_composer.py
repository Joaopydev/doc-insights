from typing import Callable

from src.processing.application.use_cases.textract_completed import TextractCompletedUseCase
from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository
from src.processing.infrastructure.extractors.text_extractor import TextExtractor

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.storage.s3 import S3Client


class TextractCompletedComposer:

    @staticmethod
    def compose() -> Callable:
        repo = DocumentProcessingRepository(DynamoDBClient())
        use_case = TextractCompletedUseCase(
            document_processing_repository=repo,
            text_extractor=TextExtractor(),
            storage_port=S3Client()
        )

        return use_case.execute
