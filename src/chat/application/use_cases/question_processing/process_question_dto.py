from pydantic import BaseModel


class ProcessQuestionInput(BaseModel):
    message_id: str
    document_id: str
    cache_key: str
