from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.application.ports.document_repository import DocumentRepository
from src.chat.domain.entities.conversation import Conversation

from src.shared.application.events.create_conversation_event import CreateConversationEvent

from src.shared.domain.value_objects.document_status import DocumentStatus


class CreateConversationUseCase:

    def __init__(
        self,
        chat_repository: ChatRepository,
        document_repository: DocumentRepository,
    ):
        self.chat_repository = chat_repository
        self.document_repository = document_repository

    def execute(self, event: CreateConversationEvent) -> None:

        document = self.document_repository.get_document_by_id(event.document_id)
        if document.status != DocumentStatus.READY:
            return

        if document.user_id != event.user_id:
            return

        conversation = Conversation.create(
            document_id=event.document_id,
            user_id=event.user_id
        )
        self.chat_repository.save_conversation(conversation)
        self.document_repository.update_conversation_id(
            document_id=document.id,
            conversation_id=conversation.id,
        )
