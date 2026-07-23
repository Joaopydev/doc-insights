from dataclasses import dataclass

from src.shared.application.events.domain_event import DomainEvent


@dataclass(frozen=True)
class QuestionAskedEvent(DomainEvent):
    message_id: str
    conversation_id: str
    document_id: str
    user_id: str

    @property
    def source(self) -> str:
        return "docinsight.chat"

    @property
    def detail_type(self) -> str:
        return "QuestionAsked"

    @property
    def detail(self) -> dict:
        return {
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "document_id": self.document_id,
            "user_id": self.user_id,
        }
