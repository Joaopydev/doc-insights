from src.errors.types.app_exception import AppException
from src.shared.presentation.http_types.http_response import HTTPResponse


class ExceptionResponseBuilder:

    @staticmethod
    def build(error: Exception) -> HTTPResponse:
        if isinstance(error, AppException):
            return HTTPResponse(
                status_code=error.status_code,
                body={
                    "errors": {
                        "title": error.name,
                        "detail": error.message,
                    }
                }
            )

        return HTTPResponse(
            status_code=500,
            body={
                "errors": {
                    "title": "Internal Server Error",
                    "detail": str(error),
                }
            }
        )
