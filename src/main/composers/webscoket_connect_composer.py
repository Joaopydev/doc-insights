from typing import Callable

from src.chat.application.use_cases.websocket.connect import WebSocketConnectUseCase
from src.chat.presentation.controllers.websocket_connect_controller import WebSocketConnectController
from src.chat.infrastructure.repositories.connection_repository import ConnectionRepository
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class WebSocketConnectComposer:

    @staticmethod
    def compose() -> Callable:
        connection_repository = ConnectionRepository(DynamoDBClient())
        use_case = WebSocketConnectUseCase(connection_repository)
        controller = WebSocketConnectController(use_case)
        return controller.handle
