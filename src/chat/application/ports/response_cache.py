from typing import Optional
from abc import ABC, abstractmethod


class ResponseCache(ABC):

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        pass


    @abstractmethod
    def set(self, key: str, value: str, ttl: int) -> None:
        pass

    @abstractmethod
    def create_cache_key(self, document_id: str, question: str) -> str:
        pass
