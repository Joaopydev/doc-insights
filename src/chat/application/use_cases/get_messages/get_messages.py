from src.chat.application.use_cases.get_messages.get_messsages_dto import (
    GetMessagesInput,
    GetMessagesOutPut,
)
from src.chat.application.ports.chat_repository import ChatRepository
from src.errors.types.conversation_not_found import ConversationNotFound


class GetMessagesUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    def execute(
        self,
        input_dto: GetMessagesInput
    ) -> GetMessagesOutPut:

        conversation = self.chat_repository.get_conversation_by_id(input_dto.conversation_id)
        if not conversation or conversation.user_id != input_dto.user_id:
            raise ConversationNotFound("Conversation not found.")

        messages = self.chat_repository.get_messages(input_dto.conversation_id)
        return GetMessagesOutPut(messages=messages)
