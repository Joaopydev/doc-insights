from src.errors.types.app_exception import AppException


class DocumentNotReady(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=401,
            name="Conflict",
            message=message
        )
