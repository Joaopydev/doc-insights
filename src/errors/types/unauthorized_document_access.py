from src.errors.types.app_exception import AppException


class UnauthorizedDocumentAccess(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=403,
            name="Forbidden",
            message=message
        )
