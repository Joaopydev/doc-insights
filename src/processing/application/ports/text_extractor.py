from abc import ABC, abstractmethod
from typing import List, Dict


class TextExtractor(ABC):

    @abstractmethod
    def start_extraction(self, storage_key: str, document_id: str) -> str:
        pass

    @abstractmethod
    def get_document_text(self, job_id: str) -> str:
        pass

    @abstractmethod
    def _blocks_to_text(self, blocks: List[Dict]) -> str:
        pass
