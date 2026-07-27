from abc import ABC, abstractmethod
from typing import List

from src.processing.domain.entities.chunk import DocumentChunk


class VectorRepository(ABC):

    @abstractmethod
    def store_chunks(
        self,
        chunks: List[DocumentChunk]
    ) -> None:
        pass

    @abstractmethod
    def semantic_similarity_search(
        self,
        embedding: List[float],
        document_id: str,
        limit: int = 5
    ) -> List[DocumentChunk]:
        pass
