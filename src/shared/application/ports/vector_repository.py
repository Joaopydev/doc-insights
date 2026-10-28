from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.chunk import DocumentChunk


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

    @abstractmethod
    def delete_chunks_by_document_id(self, document_id: str) -> None:
        pass
