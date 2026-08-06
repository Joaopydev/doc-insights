from typing import Callable

from src.chat.application.use_cases.websocket.post_to_connection import WebSocketPostToConnectionUseCase
from src.chat.infrastructure.repositories.connection_repository import ConnectionRepository
from src.chat.infrastructure.repositories.chat_repository import ChatRepository
from src.chat.infrastructure.websocket.webscoket_service import WebSocketService
from src.chat.infrastructure.gateway.gateway_client import GatewayClient

from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class WebSocketPostToConnectionComposer:

    @staticmethod
    def compose() -> Callable:
        db_client = DynamoDBClient()
        connection_repository = ConnectionRepository(db_client=db_client)
        websocket_service = WebSocketService(
            gateway_client=GatewayClient(),
            connection_repository=connection_repository
        )
        chat_repository = ChatRepository(db_client=db_client)
        use_case = WebSocketPostToConnectionUseCase(
            websocket_service=websocket_service,
            chat_repository=chat_repository,
            connection_repository=connection_repository
        )
        return use_case.execute
