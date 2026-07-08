from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.processing.application.ports.chunk_generator import (
    ChunkGenerator as ChunkGeneratorInterface
)


class RecursiveChunkGenerator(ChunkGeneratorInterface):

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000,
            chunk_overlap=200,
        )

    def generate_chunks(self, text: str) -> List[str]:
        return self.splitter.split_text(text=text)
