from src.chat.application.use_cases.get_conversation.get_conversation_dto import (
    GetConversationByIdInput,
    GetConversationByIdOutput,
)
from src.chat.application.ports.chat_repository import ChatRepository
from src.errors.types.conversation_not_found import ConversationNotFound


class GetConversationByIdUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    def execute(
        self,
        input_dto: GetConversationByIdInput
    ) -> GetConversationByIdOutput:

        conversation = self.chat_repository.get_conversation_by_id(input_dto.conversation_id)
        if not conversation or conversation.user_id != input_dto.user_id:
            raise ConversationNotFound("Conversation not found.")

        return GetConversationByIdOutput(conversation=conversation)
