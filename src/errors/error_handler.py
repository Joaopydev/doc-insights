from src.errors.types.app_exception import AppException
from src.shared.presentation.http_types.http_response import HTTPResponse


class ExceptionResponseBuilder:

    def __init__(self, error: Exception) -> None:
        self._error = error

    def handle(self) -> HTTPResponse:
        if isinstance(self._error, AppException):
            return HTTPResponse(
                status_code=self._error.status_code,
                body={
                    "errors": {
                        "title": self._error.name,
                        "detail": self._error.message,
                    }
                }
            )

        return HTTPResponse(
            status_code=500,
            body={
                "errors": {
                    "title": "Internal Server Error",
                    "detail": self._error.message,
                }
            }
        )
