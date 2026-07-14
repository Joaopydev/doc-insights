from abc import ABC, abstractmethod
from typing import List


class AIClient(ABC):

    @abstractmethod
    async def embedings_create(self, chunks: List[str]) -> List[float]:
        pass
