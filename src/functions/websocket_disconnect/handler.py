from typing import Dict, Any

from src.errors.error_handler import ExceptionResponseBuilder
from src.main.composers.websocket_disconnect_composer import WebSocketDisconnectComposer
from src.main.adapters.api_gateway_request_adapter import APIGatewayRequestAdapter


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        http_response = APIGatewayRequestAdapter.adapt(
            event=event,
            controller=WebSocketDisconnectComposer.compose(),
            auth_required=False
        )
    except Exception as e:
        http_response = ExceptionResponseBuilder.build(e)

    return http_response.to_dict()
