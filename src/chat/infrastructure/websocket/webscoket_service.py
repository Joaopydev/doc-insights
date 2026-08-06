import logging

from botocore.exceptions import ClientError

from src.chat.application.ports.websocket_service import (
    WebSocketService as WebSocketServiceInterface
)
from src.chat.application.ports.gateway_client import GatewayClient
from src.chat.application.ports.connection_repository import ConnectionRepository


class WebSocketService(WebSocketServiceInterface):

    def __init__(
        self,
        gateway_client: GatewayClient,
        connection_repository: ConnectionRepository,
    ) -> None:

        self.gateway_client = gateway_client
        self.connection_repository = connection_repository


    def post_to_connection(
        self,
        connection_id: str,
        data: dict
    ) -> None:
        try:
            self.gateway_client.post_to_connection(connection_id, data)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'GoneException':
                logging.info("Client %s desconnected. Cleaning database.", connection_id)
                try:
                    self.connection_repository.delete_connection(connection_id)
                except Exception as db_err:
                    logging.error("Failed to delete connection on DynamoDB: %s", db_err)
            else:
                logging.error("Client API Gateway WebSocket Error: %s", e)
                raise
        except Exception as e:
            logging.error("Generic failure to send message via WebSocket.: %s", e)
            raise
