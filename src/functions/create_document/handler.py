from typing import Dict, Any

from src.main.adapters.api_gateway_request_adapter import APIGatewayRequestAdapter
from src.main.composers.create_document_composer import CreateDocumentComposer


def handler(event: Dict[str, Any], context: Any):

    response = APIGatewayRequestAdapter.adapt(
        event=event,
        use_case=CreateDocumentComposer.compose()
    )

    return {
        "statusCode": response.status_code,
        "headers": response.headers,
        "body": response.body
    }
