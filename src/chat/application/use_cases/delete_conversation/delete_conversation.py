from src.chat.application.use_cases.delete_conversation.delete_conversation_dto import (
    DeleteConversationInput,
)
from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.application.ports.document_repository import DocumentRepository

from src.shared.application.ports.storage_port import StoragePort
from src.shared.application.ports.vector_repository import VectorRepository

from src.errors.types.conversation_not_found import ConversationNotFound


class DeleteConversationUseCase:

    def __init__(
        self,
        chat_repository: ChatRepository,
        document_repository: DocumentRepository,
        vector_repository: VectorRepository,
        storage_port: StoragePort,
    ) -> None:
        self.chat_repository = chat_repository
        self.document_repository = document_repository
        self.vector_repository = vector_repository
        self.storage_port = storage_port

    def execute(self, input_dto: DeleteConversationInput) -> None:

        conversation = self.chat_repository.get_conversation_by_id(input_dto.conversation_id)
        if not conversation or conversation.user_id != input_dto.user_id:
            raise ConversationNotFound("Conversation not found.")

        document = self.document_repository.get_document_by_id(conversation.document_id)

        self.vector_repository.delete_chunks_by_document_id(document.id)
        self.storage_port.delete_object(document.s3_key.get_value())
        self.storage_port.delete_object(document.extracted_text_key.get_value())
        self.document_repository.delete_document_by_id(document.id)

        self.chat_repository.delete_messages_by_conversation_id(conversation.id)
        self.chat_repository.delete_conversation_by_id(conversation.id)
