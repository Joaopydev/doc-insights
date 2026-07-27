from abc import ABC, abstractmethod
from typing import List


class AIClient(ABC):

    @abstractmethod
    async def create_embeddings(self, chunks: List[str]) -> List[List[float]]:
        pass
