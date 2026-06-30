from typing import Callable

from src.processing.application.use_cases.start_extraction_text import StartExtractionTextUseCase
from src.processing.infrastructure.repositories.document_processing_repository import DocumentProcessingRepository
from src.processing.infrastructure.extractors.text_extractor import TextExtractor

from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class StartExtractionTextComposer:

    @staticmethod
    def compose() -> Callable:
        repo = DocumentProcessingRepository(DynamoDBClient())
        use_case = StartExtractionTextUseCase(
            document_processing_repository=repo,
            text_extractor=TextExtractor(),
        )

        return use_case.execute
