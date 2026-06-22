from src.processing.application.ports.document_processing_repository import DocumentProcessingRepository

from src.shared.domain.value_objects.document_status import DocumentStatus


class ProcessDocumentUseCase:

    def __init__(self, document_processing_repository: DocumentProcessingRepository):
        self.document_processing_repository = document_processing_repository

    def execute(self, storage_key: str):
        document = self.document_processing_repository.get_document_by_storage_key(storage_key)
        if not document:
            return

        if document.status in ["FAILED", "COMPLETED", "EXTRACTING"]:
            return

        self.document_processing_repository.update_status(
            document_id=document.id,
            status=DocumentStatus.EXTRACTING.value
        )
