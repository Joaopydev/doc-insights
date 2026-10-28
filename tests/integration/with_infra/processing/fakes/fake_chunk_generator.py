from typing import List

from src.processing.application.ports.chunk_generator import ChunkGenerator
from src.shared.domain.entities.chunk import DocumentChunk


class FakeChunkGenerator(ChunkGenerator):

    def generate_chunks(self, text: str) -> List[str] :
        return text.split("/")

    def generate_document_chunks(
        self,
        document_id: str,
        chunks:  List[str],
        embeddings: List[List[float]]
    ) -> None:

        document_chunks = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            document_chunk = DocumentChunk.create(
                document_id=document_id,
                chunk_order=i,
                content=chunk,
                embedding=embedding
            )
            document_chunks.append(document_chunk)

        return document_chunks
