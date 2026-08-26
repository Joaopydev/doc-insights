from src.upload.application.ports.document_repository import (
    DocumentRepository as DocumentRepositoryInterface
)
from src.upload.application.use_cases.create_document_dto import (
    CreateDocumentInput,
    CreateDocumentOutput,
)

from src.shared.domain.entities.document import Document
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
        create_document_input: CreateDocumentInput
    ) -> CreateDocumentOutput:

        document = Document.create(
            user_id=create_document_input.user_id,
            metadata=create_document_input.metadata.model_dump()
        )
        self.document_repository.insert_document(document)

        presigned_url = self.storage_port.generate_presigned_url(
            file_key=document.s3_key.get_value(),
            content_type=document.metadata.content_type,
            expire_in=3600
        )

        return CreateDocumentOutput(
            document=document,
            presigned_url=presigned_url
        )
