from pydantic import BaseModel

from src.chat.domain.entities.chat_message import ChatMessage


class AskQuestionInput(BaseModel):
    user_id: str
    document_id: str
    question: str


class AskQuestionOutput(BaseModel):
    message: ChatMessage
