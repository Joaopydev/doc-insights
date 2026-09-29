from dataclasses import dataclass

from src.shared.application.events.domain_event import DomainEvent


@dataclass(frozen=True)
class CreateConversationEvent(DomainEvent):
    user_id: str
    document_id: str

    @property
    def source(self) -> str:
        return "docinsight.chat"

    @property
    def detail_type(self) -> str:
        return "DocumentReady"

    @property
    def detail(self) -> dict:
        return {
            "user_id": self.user_id,
            "document_id": self.document_id,
        }
