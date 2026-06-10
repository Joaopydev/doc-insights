from src.upload.application.ports.document_repository import (
    DocumentRepository as DocumentRepositoryInterface
)
from src.upload.domain.entities.document import Document

from src.shared.application.ports.storage_port import StoragePort
from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse


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
        request: HTTPRequest
    ) -> HTTPResponse:

        document = Document.create(
            user_id=request.body["user_id"],
            metadata=request.body["metadata"]
        )
        self.document_repository.save(document)

        presigned_url = self.storage_port.get_presigned_url(
            document_key=document.id,
            content_type=request.metadata.content_type,
            expire_in=3600
        )

        return HTTPResponse(
            status_code=201,
            body={
                "document": document.to_dict(),
                "presigned_url": presigned_url
            }
        )
