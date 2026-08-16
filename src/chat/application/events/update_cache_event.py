from dataclasses import dataclass

from src.shared.application.events.domain_event import DomainEvent


@dataclass(frozen=True)
class UpdateCacheEvent(DomainEvent):
    cache_key: str
    generated_response: str

    @property
    def source(self) -> str:
        return "docinsight.chat"

    @property
    def detail_type(self) -> str:
        return "UpdateCache"

    @property
    def detail(self) -> dict:
        return {
            "cache_key": self.cache_key,
            "generated_response": self.generated_response,
        }
