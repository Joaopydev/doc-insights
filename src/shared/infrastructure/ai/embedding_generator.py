from typing import List

from src.shared.application.ports.embedding_generator import (
    EmbeddingGenerator as EmbddingGeneratorInterface,
)
from src.shared.application.ports.ai_client import AIClient


class EmbeddingGenerator(EmbddingGeneratorInterface):

    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client

    async def generate_embedding(self, texts: List[str]) -> List[List[float]]:
        return await self.ai_client.create_embeddings(texts)
