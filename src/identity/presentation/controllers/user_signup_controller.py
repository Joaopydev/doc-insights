from src.identity.application.use_cases.signup.user_signup import UserSignupUseCase
from src.identity.application.use_cases.signup.user_signup_dto import SignupInput

from src.shared.presentation.interfaces.controller_interface import ControllerInterface
from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse


class UserSignupController(ControllerInterface):

    def __init__(self, use_case: UserSignupUseCase):
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = SignupInput(
            email=request.body["email"],
            name=request.body["name"],
            password=request.body["password"]
        )
        output = self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=201,
            body={"access_token": output.access_token}
        )
