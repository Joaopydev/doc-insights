from pydantic import BaseModel
from src.chat.domain.entities.conversation import Conversation


class GetConversationByIdInput(BaseModel):
    user_id: str
    conversation_id: str


class GetConversationByIdOutput(BaseModel):
    conversation: Conversation
