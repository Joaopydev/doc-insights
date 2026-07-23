from abc import ABC, abstractmethod


class DomainEvent(ABC):

    @property
    @abstractmethod
    def source(self) -> str:
        ...

    @property
    @abstractmethod
    def detail_type(self) -> str:
        ...

    @property
    @abstractmethod
    def detail(self) -> dict:
        ...
