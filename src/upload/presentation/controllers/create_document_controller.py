from src.upload.application.use_cases.create_document import CreateDocumentUseCase
from src.upload.application.use_cases.create_document_dto import CreateDocumentInput

from src.shared.presentation.interfaces.controller_interface import ControllerInterface
from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse


class CreateDocumentController(ControllerInterface):

    def __init__(self, use_case: CreateDocumentUseCase):
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = CreateDocumentInput(
            user_id=request.user_id,
            metadata=request.body["metadata"]
        )

        output = self.use_case.execute(input_data)
        return HTTPResponse(
            status_code=201,
            body={
                "document": output.document.to_dict(),
                "presigned_url": output.presigned_url
            }
        )
