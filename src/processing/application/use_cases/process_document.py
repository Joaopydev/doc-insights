from src.processing.application.ports.document_processing_repository import DocumentProcessingRepository
from src.processing.application.ports.text_extractor import TextExtractor

from src.shared.domain.value_objects.document_status import DocumentStatus
from src.shared.application.ports.storage_port import StoragePort


class ProcessDocumentUseCase:

    def __init__(
        self,
        document_processing_repository: DocumentProcessingRepository,
        text_extractor: TextExtractor,
        storage_port: StoragePort,
    ):
        self.document_processing_repository = document_processing_repository
        self.text_extractor = text_extractor
        self.storage_port = storage_port

    def execute(self, storage_key: str):
        document = self.document_processing_repository.get_document_by_storage_key(storage_key)
        if not document:
            return

        if document.status in [
            DocumentStatus.FAILED,
            DocumentStatus.COMPLETED,
            DocumentStatus.EXTRACTING,
            DocumentStatus.EXTRACTED,
        ]:
            return

        self.document_processing_repository.update_status(
            document_id=document.id,
            status=DocumentStatus.EXTRACTING.value
        )

        raw_document = self.storage_port.read_object_content(document.s3_key.get_value())
        extracted_text = self.text_extractor.extract(raw_document)

        print(extracted_text)
