from src.upload.application.ports.document_repository import (
    DocumentRepository as DocumentRepositoryInterface
)
from src.upload.domain.entities.document import Document
from src.upload.application.dto.create_document_input import CreateDocumentInput
from src.upload.application.dto.create_document_output import CreateDocumentOutput

from src.shared.application.ports.storage_port import StoragePort



class CreateDocumentUseCase:

    def __init__(
        self,
        document_repository: DocumentRepositoryInterface,
        storage_port: StoragePort
    ):
        self.document_repository = document_repository
        self.storage_port = storage_port

    def execute(
        self,
        request: CreateDocumentInput
    ) -> CreateDocumentOutput:

        document = Document.create(
            user_id=request.user_id,
            metadata=request.metadata
        )
        self.document_repository.save(document)

        presigned_url = self.storage_port.get_presigned_url(
            document_key=document.id,
            content_type=request.metadata.content_type,
            expire_in=3600
        )

        return CreateDocumentOutput(
            document=document,
            presigned_url=presigned_url,
        )
