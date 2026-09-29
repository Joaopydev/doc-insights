from src.upload.application.use_cases.get.dto import (
    GetDocumentByIdInput,
    GetDocumentByIdOutput,
)
from src.upload.application.ports.document_repository import DocumentRepository

from src.errors.types.unauthorized_document_access import UnauthorizedDocumentAccess
from src.errors.types.document_not_found import DocumentNotFound


class GetDocumentByIdUseCase:

    def __init__(self, document_repository: DocumentRepository) -> None:
        self.document_repository = document_repository

    def execute(self, get_document_input: GetDocumentByIdInput) -> GetDocumentByIdOutput:

        document = self.document_repository.get_document_by_id(get_document_input.document_id)
        if not document:
            raise DocumentNotFound("Document not found.")

        if document.user_id != get_document_input.user_id:
            raise UnauthorizedDocumentAccess("The current user is not the owner of the document")

        return GetDocumentByIdOutput(document=document)
