from src.upload.application.ports.document_repository import DocumentRepository

from src.upload.application.use_cases.delete.dto import DeleteDocumentInput

from src.errors.types.unauthorized_document_access import UnauthorizedDocumentAccess
from src.errors.types.document_not_found import DocumentNotFound



class DeleteDocumentUseCase:

    def __init__(self, document_repository: DocumentRepository) -> None:
        self.document_repository = document_repository

    def execute(
        self,
        delete_document_input: DeleteDocumentInput
    ) -> None:

        document = self.document_repository.get_document_by_id(delete_document_input.document_id)
        if not document:
            raise DocumentNotFound("Document not found.")

        if document.user_id != delete_document_input.user_id:
            raise UnauthorizedDocumentAccess("The current user is not the owner of the document")

        self.document_repository.delete_document_by_id(document.id)
