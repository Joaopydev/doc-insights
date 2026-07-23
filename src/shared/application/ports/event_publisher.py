from abc import ABC, abstractmethod

from src.shared.application.events.domain_event import DomainEvent


class EventPublisher(ABC):

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        pass
