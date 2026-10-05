from typing import List
from pydantic import BaseModel

from src.chat.domain.entities.conversation import Conversation


class ListUserConversationsOutput(BaseModel):
    conversations: List[Conversation]
