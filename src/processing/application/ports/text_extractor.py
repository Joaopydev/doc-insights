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

    @abstractmethod
    def _clean_line_texts(self, line_texts: list[str]) -> list[str]:
        pass

    @abstractmethod
    def _normalize(self, text: str) -> str:
        pass

    @abstractmethod
    def _is_short_token(self, text: str) -> bool:
        pass

    @abstractmethod
    def _detect_boilerplate(
        self, page_paragraphs: list[tuple[int, str]], total_pages: int
    ) -> set[str]:
        pass
