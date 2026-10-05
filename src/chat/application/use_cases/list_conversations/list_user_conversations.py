from src.chat.application.use_cases.list_conversations.list_user_conversations_dto import ListUserConversationsOutput
from src.chat.application.ports.chat_repository import ChatRepository


class ListUserConversationsUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    def execute(
        self,
        user_id: str
    ) -> ListUserConversationsOutput:

        conversations = self.chat_repository.list_conversations_by_user_id(user_id)
        return ListUserConversationsOutput(conversations=conversations)
