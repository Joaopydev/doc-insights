from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.processing.application.ports.chunk_generator import (
    ChunkGenerator as ChunkGeneratorInterface
)
from src.shared.domain.entities.chunk import DocumentChunk


class RecursiveChunkGenerator(ChunkGeneratorInterface):

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base",
            chunk_size=850,
            chunk_overlap=150,
        )

    def generate_chunks(self, text: str) -> List[str]:
        return self.splitter.split_text(text=text)

    def generate_document_chunks(
        self,
        document_id: str,
        chunks: List[str],
        embeddings: List[List[float]]
    ) -> List[DocumentChunk]:

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
