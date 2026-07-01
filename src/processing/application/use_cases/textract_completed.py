from src.processing.application.ports.document_processing_repository import DocumentProcessingRepository
from src.processing.application.ports.text_extractor import TextExtractor

from src.shared.domain.value_objects.document_status import DocumentStatus
from src.shared.application.ports.storage_port import StoragePort



class TextractCompletedUseCase:

    def __init__(
        self,
        document_processing_repository: DocumentProcessingRepository,
        text_extractor: TextExtractor,
        storage_port: StoragePort
    ):
        self.text_extractor = text_extractor
        self.document_processing_repository = document_processing_repository
        self.storage_port = storage_port


    def execute(self, job_id: str):
        document = self.document_processing_repository.get_document_by_textract_job_id(job_id)
        if not document:
            return

        if document.status != DocumentStatus.EXTRACTING:
            return

        document_text = self.text_extractor.get_document_text(job_id)
        self.storage_port.put_object(
            key=document.extracted_text_key.get_value(),
            body=document_text.encode("utf-8"),
            content_type="text/plain"
        )

        self.document_processing_repository.update_status(
            document_id=document.id,
            status=DocumentStatus.EXTRACTED
        )
