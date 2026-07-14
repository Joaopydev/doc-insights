from abc import ABC, abstractmethod
from typing import List


class EmbeddingGenerator(ABC):

    @abstractmethod
    async def generate_embedding(self, chunks: List[str]) -> List[float]:
        pass
