from src.identity.application.use_cases.login.user_login import UserLoginUseCase
from src.identity.application.use_cases.login.user_login_dto import LoginInput

from src.shared.presentation.interfaces.controller_interface import ControllerInterface
from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse


class UserLoginController(ControllerInterface):

    def __init__(self, use_case: UserLoginUseCase):
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = LoginInput(
            email=request.body["email"],
            password=request.body["password"]
        )
        output = self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=200,
            body={"access_token": output.access_token}
        )
