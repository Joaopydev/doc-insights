import json
from typing import Callable

from src.main.middlewares.authentication_middleware import AuthenticationMiddleware

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.infrastructure.security.jwt_service import JWTService


class APIGatewayRequestAdapter:

    @staticmethod
    def adapt(event: dict, use_case: Callable, auth_required: bool = False) -> HTTPResponse:
        user_id = None

        if auth_required:
            auth_middleware = AuthenticationMiddleware(JWTService())
            user_id = auth_middleware.handle(event.get("headers", {}))

        http_request = HTTPRequest(
            body=json.loads(event.get("body", "{}")),
            params=event.get("pathParameters", {}),
            query=event.get("queryStringParameters", {}),
            user_id=user_id
        )

        return use_case(http_request)
