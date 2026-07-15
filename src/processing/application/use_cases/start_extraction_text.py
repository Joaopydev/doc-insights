from src.processing.application.ports.document_processing_repository import DocumentProcessingRepository
from src.processing.application.ports.text_extractor import TextExtractor

from src.shared.domain.value_objects.document_status import DocumentStatus


class StartExtractionTextUseCase:

    def __init__(
        self,
        document_processing_repository: DocumentProcessingRepository,
        text_extractor: TextExtractor,
    ):
        self.document_processing_repository = document_processing_repository
        self.text_extractor = text_extractor

    def execute(self, storage_key: str):
        document = self.document_processing_repository.get_document_by_storage_key(storage_key)
        if not document:
            return

        if document.status in [
            DocumentStatus.FAILED,
            DocumentStatus.READY,
            DocumentStatus.EXTRACTING,
            DocumentStatus.EXTRACTED,
            DocumentStatus.INDEXING,
        ]:
            return

        self.document_processing_repository.update_status(
            document_id=document.id,
            status=DocumentStatus.EXTRACTING.value
        )

        job_id = self.text_extractor.start_extraction(
            storage_key=document.s3_key.get_value(),
            document_id=document.id,
        )
        self.document_processing_repository.update_textract_job_id(
            document_id=document.id,
            job_id=job_id,
        )
