from dataclasses import dataclass

from src.shared.application.events.domain_event import DomainEvent


@dataclass(frozen=True)
class QuestionAnsweredEvent(DomainEvent):
    conversation_id: str

    @property
    def source(self) -> str:
        return "docinsight.chat"

    @property
    def detail_type(self) -> str:
        return "QuestionAnswered"

    @property
    def detail(self) -> dict:
        return {
            "conversation_id": self.conversation_id
        }
