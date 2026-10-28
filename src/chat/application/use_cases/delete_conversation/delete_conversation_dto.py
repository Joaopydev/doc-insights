from pydantic import BaseModel


class DeleteConversationInput(BaseModel):
    user_id: str
    conversation_id: str
