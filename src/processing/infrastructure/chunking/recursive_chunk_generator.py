from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.processing.application.ports.chunk_generator import (
    ChunkGenerator as ChunkGeneratorInterface
)


class RecursiveChunkGenerator(ChunkGeneratorInterface):

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name="cl100k_base",
            chunk_size=850,
            chunk_overlap=150,
        )

    def generate_chunks(self, text: str) -> List[str]:
        return self.splitter.split_text(text=text)
