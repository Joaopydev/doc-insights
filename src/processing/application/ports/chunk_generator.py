from abc import ABC, abstractmethod
from typing import List

from src.processing.domain.entities.chunk import DocumentChunk


class ChunkGenerator(ABC):

    @abstractmethod
    def generate_chunks(self, text: str) -> List[str]:
        pass

    @abstractmethod
    def generate_document_chunks(
        self, document_id: str,
        chunks: List[str],
        embeddings: List[List[float]]
    ) -> List[DocumentChunk]:
        pass
