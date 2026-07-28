from typing import List

from src.processing.domain.entities.chunk import DocumentChunk


class ContextBuilder:

    @staticmethod
    def build(chunks: List[DocumentChunk]) -> str:
        return "\n\n".join(chunk.content for chunk in chunks)
