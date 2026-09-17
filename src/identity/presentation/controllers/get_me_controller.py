from src.identity.application.use_cases.me.get_user import GetUserUseCase

from src.shared.presentation.interfaces.controller_interface import ControllerInterface
from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse


class GetMeController(ControllerInterface):

    def __init__(self, use_case: GetUserUseCase):
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        output = self.use_case.execute(request.user_id)

        return HTTPResponse(
            status_code=200,
            body={"user": output.to_dict()}
        )
