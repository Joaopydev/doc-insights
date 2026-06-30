from abc import ABC, abstractmethod


class TextExtractor(ABC):

    @abstractmethod
    def start_extraction(self, storage_key: str, document_id: str) -> str:
        pass
