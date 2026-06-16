from src.errors.types.app_exception import AppException


class AccesTokenNotProvided(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=401,
            name="Unauthorized",
            message=message
        )
