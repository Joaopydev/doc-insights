from src.identity.application.ports.user_repository import (
    UserRepository as UserRepositoryInterface
)
from src.identity.application.ports.password_hasher import PasswordHasher
from src.identity.domain.entities.user import UserIdentity
from src.identity.application.use_cases.signup.user_signup_dto import (
    SignupInput,
    SignupOutput,
)

from src.shared.application.ports.jwt_port import JWTPort
from src.errors.types.conflict_exception import EmailAlreadyExists


class UserSignupUseCase:

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
        signup_input: SignupInput,
    ) -> SignupOutput:

        existing_user = self.user_repository.get_by_email(signup_input.email)
        if existing_user:
            raise EmailAlreadyExists()

        hashed_password = self.password_hasher.hash(
            signup_input.password
        )
        user = UserIdentity.create(
            name=signup_input.name,
            email=signup_input.email,
            password=hashed_password,
        )
        self.user_repository.insert_user(user)
        access_token = self.jwt_port.signin_access_token(user.id)

        return SignupOutput(access_token=access_token)
