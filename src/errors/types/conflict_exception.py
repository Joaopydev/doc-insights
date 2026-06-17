from src.errors.types.app_exception import AppException


class ConflictException(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=409,
            name="ConflictException",
            message=message
        )

class EmailAlreadyExists(ConflictException):
    def __init__(self):
        super().__init__("Email already exists")
