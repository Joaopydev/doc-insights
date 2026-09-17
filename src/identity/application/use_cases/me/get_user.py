from src.identity.domain.entities.user import UserIdentity
from src.identity.application.ports.user_repository import UserRepository
from src.errors.types.user_not_found import UserNotFound

class GetUserUseCase:

    def __init__(
        self,
        user_repository: UserRepository
    ) -> None:

        self.user_repository = user_repository

    def execute(self, user_id: str) -> UserIdentity:

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFound("User not found")

        return user
