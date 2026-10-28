from typing import List

from src.shared.application.ports.vector_repository import VectorRepository
from src.shared.domain.entities.chunk import DocumentChunk


class FakeVectorRepository(VectorRepository):
    def __init__(self):
        self.stored_chunks = []

    def store_chunks(self, chunks: List[DocumentChunk]):
        self.stored_chunks.append({chunks[0].document_id: chunks})

    def semantic_similarity_search(self, embedding, document_id, limit = 5):
        raise NotImplementedError
