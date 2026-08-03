from typing  import List
from pydantic import BaseModel

from src.chat.domain.entities.chat_message import ChatMessage


class GetMessagesInput(BaseModel):
    user_id: str
    conversation_id: str


class GetMessagesOutPut(BaseModel):
    messages: List[ChatMessage]
