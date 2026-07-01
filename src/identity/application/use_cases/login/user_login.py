from src.identity.application.ports.user_repository import (
    UserRepository as UserRepositoryInterface
)
from src.identity.application.ports.password_hasher import PasswordHasher
from src.identity.application.use_cases.login.user_login_dto import (
    LoginInput,
    LoginOutput
)

from src.shared.application.ports.jwt_port import JWTPort
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
        login_input: LoginInput,
    ) -> LoginOutput:

        user = self.user_repository.get_by_email(login_input.email)
        if not user:
            raise InvalidCredentials("Invalid Credentials.")

        is_valid_password = self.password_hasher.verify(
            password=login_input.password,
            hashed_password=user.password,
        )
        if not is_valid_password:
            raise InvalidCredentials("Invalid Credentials")

        access_token = self.jwt_port.signin_access_token(user.id)
        return LoginOutput(access_token=access_token)
