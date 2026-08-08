import json
import boto3

from src.chat.application.ports.gateway_client import (
    GatewayClient as GatewayClientInterface
)
from src.main.config.settings import settings


class GatewayClient(GatewayClientInterface):

    def __init__(self) -> None:
        self.client = boto3.client(
            service_name='apigatewaymanagementapi',
            endpoint_url=settings.websocket_endpoint
        )

    def post_to_connection(self, connection_id, data):
        return self.client.post_to_connection(
            ConnectionId=connection_id,
            Data=json.dumps(data)
        )
