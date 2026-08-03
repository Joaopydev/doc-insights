from typing import Dict, Any

from src.main.adapters.api_gateway_request_adapter import APIGatewayRequestAdapter
from src.main.composers.get_messages_composer import GetMessagesComposer
from src.errors.error_handler import ExceptionResponseBuilder


def handler(event: Dict[str, Any], context: Any):
    try:
        http_response = APIGatewayRequestAdapter.adapt(
            event=event,
            controller=GetMessagesComposer.compose(),
            auth_required=True,
        )
    except Exception as e:
        http_response = ExceptionResponseBuilder.build(e)

    return http_response.to_dict()
