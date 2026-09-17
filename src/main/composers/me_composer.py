from typing import Callable

from src.identity.application.use_cases.me.get_user import GetUserUseCase
from src.identity.presentation.controllers.get_me_controller import GetMeController
from src.identity.infrastructure.repositories.user_repository import UserRepository
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class MeComposer:

    @staticmethod
    def compose() -> Callable:
        repository = UserRepository(DynamoDBClient())
        use_case = GetUserUseCase(repository)
        controller = GetMeController(use_case)

        return controller.handle
