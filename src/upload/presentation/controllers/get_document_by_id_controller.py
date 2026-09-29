from src.upload.application.use_cases.get.get_document_by_id import GetDocumentByIdUseCase
from src.upload.application.use_cases.get.dto import GetDocumentByIdInput

from src.shared.presentation.interfaces.controller_interface import ControllerInterface
from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse


class GetDocumentByIdController(ControllerInterface):

    def __init__(self, use_case: GetDocumentByIdUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = GetDocumentByIdInput(
            user_id=request.user_id,
            document_id=request.params["document_id"]
        )

        output = self.use_case.execute(input_data)
        return HTTPResponse(
            status_code=200,
            body={
                "document": {
                    "id": output.document.id,
                    "status": output.document.status.value,
                    "created_at": output.document.created_at
                }
            }
        )
