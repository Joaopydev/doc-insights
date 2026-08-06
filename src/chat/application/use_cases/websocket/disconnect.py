from src.chat.application.ports.connection_repository import ConnectionRepository
from src.chat.application.use_cases.websocket.disconnect_dto import WebSocketDisconnectInput


class WebSocketDisconnectUseCase:
    def __init__(self, connection_repository: ConnectionRepository):
        self.connection_repository = connection_repository

    def execute(self, input_data: WebSocketDisconnectInput):
        self.connection_repository.delete_connection(input_data.connection_id)
