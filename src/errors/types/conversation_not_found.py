from src.errors.types.app_exception import AppException


class ConversationNotFound(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=404,
            name="NotFound",
            message=message
        )
