from src.identity.application.ports.user_repository import (
    UserRepository as UserRepositoryInterface
)
from src.identity.application.ports.password_hasher import PasswordHasher

from src.shared.application.ports.jwt_port import JWTPort
from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse

from src.errors.types.invalid_credentials import InvalidCredentials


class UserLoginUseCase:

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_hasher: PasswordHasher,
        jwt_port: JWTPort,

    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_port = jwt_port

    def execute(
        self,
        request: HTTPRequest,
    ) -> HTTPResponse:

        user = self.user_repository.get_by_email(request.body["email"])
        if not user:
            raise InvalidCredentials("Invalid Credentials.")

        is_valid_password = self.password_hasher.verify(
            password=request.body["password"],
            hashed_password=user.password,
        )
        if not is_valid_password:
            raise InvalidCredentials("Invaliad Credentials")

        access_token = self.jwt_port.signin_access_token(user.id)

        return HTTPResponse(
            status_code=200,
            body={"access_token": access_token}
        )
