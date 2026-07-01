from typing import Callable

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.security.jwt_service import JWTService

from src.identity.infrastructure.repositories.user_repository import UserRepository
from src.identity.application.use_cases.signup.user_signup import UserSignupUseCase
from src.identity.infrastructure.security.password_hasher import PasswordHasher
from src.identity.presentation.controllers.user_signup_controller import UserSignupController


class SingupComposer:

    @staticmethod
    def compose() -> Callable:
        db_client = DynamoDBClient()
        user_repository = UserRepository(db_client=db_client)
        use_case = UserSignupUseCase(
            user_repository=user_repository,
            password_hasher=PasswordHasher(),
            jwt_port=JWTService(),
        )
        controller = UserSignupController(use_case=use_case)
        return controller.handle
