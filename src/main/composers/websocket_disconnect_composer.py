from typing import Callable

from src.chat.application.use_cases.websocket.disconnect import WebSocketDisconnectUseCase
from src.chat.infrastructure.repositories.connection_repository import ConnectionRepository
from src.chat.presentation.controllers.websocket_disconnect_controller import WebSocketDisconnectController
from src.shared.infrastructure.dynamodb.client import DynamoDBClient


class WebSocketDisconnectComposer:

    @staticmethod
    def compose() -> Callable:
        connection_repository = ConnectionRepository(DynamoDBClient())
        use_case = WebSocketDisconnectUseCase(connection_repository)
        controller = WebSocketDisconnectController(use_case)
        return controller.handle
