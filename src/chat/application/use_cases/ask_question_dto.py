from pydantic import BaseModel


class AskQuestionInput(BaseModel):
    user_id: str
    document_id: str
    conversation_id: str
    question: str


class AskQuestionOutput(BaseModel):
    message_id: str
    conversation_id: str
