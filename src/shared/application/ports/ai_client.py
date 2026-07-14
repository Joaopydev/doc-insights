from abc import ABC, abstractmethod
from typing import List


class AIClient(ABC):

    @abstractmethod
    async def embeddings_create(self, chunks: List[str]) -> List[List[float]]:
        pass
