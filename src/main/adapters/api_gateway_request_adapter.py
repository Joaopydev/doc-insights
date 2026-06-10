import json
from typing import Callable

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse


class APIGatewayRequestAdapter:

    @staticmethod
    def adapt(event: dict, use_case: Callable) -> HTTPResponse:
        http_request = HTTPRequest(
            body=json.loads(event.get("body", "{}")),
            headers=event.get("headers", {}),
            params=event.get("pathParameters", {}),
            query=event.get("queryStringParameters", {}),
        )

        return use_case(http_request)
