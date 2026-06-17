from src.errors.types.app_exception import AppException


class InvalidCredentials(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=401,
            name="InvalidCredentials",
            message=message
        )
