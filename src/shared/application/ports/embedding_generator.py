from abc import ABC, abstractmethod
from typing import List


class EmbeddingGenerator(ABC):

    @abstractmethod
    async def generate_embedding(self, texts: List[str]) -> List[List[float]]:
        pass
