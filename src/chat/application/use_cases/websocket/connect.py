from src.chat.application.ports.connection_repository import ConnectionRepository
from src.chat.application.use_cases.websocket.connect_dto import WebSocketConnectInput
from src.chat.domain.entities.connection import Connection


class WebSocketConnectUseCase:

    def __init__(self, connection_repository: ConnectionRepository):
        self.connection_repository = connection_repository

    def execute(self, input_data: WebSocketConnectInput) -> None:
        connection = Connection.create(
            connection_id=input_data.connection_id,
            user_id=input_data.user_id
        )
        self.connection_repository.create_connection(connection)
