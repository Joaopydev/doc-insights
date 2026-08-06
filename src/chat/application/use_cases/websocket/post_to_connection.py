from src.chat.application.ports.websocket_service import WebSocketService
from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.application.ports.connection_repository import ConnectionRepository
from src.chat.application.events.question_answered_event import QuestionAnsweredEvent



class WebSocketPostToConnectionUseCase:

    def __init__(
            self,
            websocket_service: WebSocketService,
            chat_repository: ChatRepository,
            connection_repository: ConnectionRepository
        ) -> None:

        self.websocket_service = websocket_service
        self.chat_repository = chat_repository
        self.connection_repository = connection_repository

    def execute(self, event: QuestionAnsweredEvent) -> None:

        conversation = self.chat_repository.get_conversation_by_id(event.conversation_id)
        if not conversation:
            return

        connection = self.connection_repository.get_connection_by_user_id(conversation.user_id)
        if not connection:
            return

        self.websocket_service.post_to_connection(
            connection_id=connection.id,
            data={
                "conversation_id": conversation.id,
            }
        )
