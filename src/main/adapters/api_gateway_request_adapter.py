import json
from typing import Callable

from src.main.middlewares.authentication_middleware import AuthenticationMiddleware

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.infrastructure.security.jwt_service import JWTService


class APIGatewayRequestAdapter:

    @staticmethod
    def adapt(event: dict, controller: Callable, auth_required: bool = False) -> HTTPResponse:
        user_id = None

        if auth_required:
            auth_middleware = AuthenticationMiddleware(JWTService())
            user_id = auth_middleware.handle(
                headers=event.get("headers", {}),
                query_params=event.get("queryStringParameters", {}),
            )

        http_request = HTTPRequest(
            body=json.loads(event.get("body", "{}")),
            params=event.get("pathParameters", {}),
            query=event.get("queryStringParameters", {}),
            user_id=user_id,
            connection_id=event.get("requestContext", {}).get("connectionId")
        )

        return controller(http_request)
