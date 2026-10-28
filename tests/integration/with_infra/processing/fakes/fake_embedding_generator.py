from typing import List
from src.shared.application.ports.embedding_generator import EmbeddingGenerator


class FakeEmbeddingGenerator(EmbeddingGenerator):

    async def generate_embedding(self, texts: List[str]) -> List[List[float]]:
        return [[0.1, 0.2, 0.3, 0.4] for _ in texts]
