from typing import Callable

from src.shared.infrastructure.dynamodb.client import DynamoDBClient
from src.shared.infrastructure.security.jwt_service import JWTService

from src.identity.infrastructure.repositories.user_repository import UserRepository
from src.identity.application.use_cases.login.user_login import UserLoginUseCase
from src.identity.infrastructure.security.password_hasher import PasswordHasher
from src.identity.presentation.controllers.user_login_controller import UserLoginController


class SinginComposer:

    @staticmethod
    def compose() -> Callable:
        db_client = DynamoDBClient()
        user_repository = UserRepository(db_client=db_client)
        use_case = UserLoginUseCase(
            user_repository=user_repository,
            password_hasher=PasswordHasher(),
            jwt_port=JWTService(),
        )
        controller = UserLoginController(use_case=use_case)
        return controller.handle
