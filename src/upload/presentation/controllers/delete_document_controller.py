from src.upload.application.use_cases.delete.dto import DeleteDocumentInput
from src.upload.application.use_cases.delete.delete_document import DeleteDocumentUseCase

from src.shared.presentation.interfaces.controller_interface import ControllerInterface
from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse


class DeleteDocumentController(ControllerInterface):

    def __init__(self, use_case: DeleteDocumentUseCase):
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = DeleteDocumentInput(
            user_id=request.user_id,
            document_id=request.body["document_id"]
        )

        self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=200,
            body={}
        )
