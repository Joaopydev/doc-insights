from abc import ABC, abstractmethod
from typing import List


class ChunkGenerator(ABC):

    @abstractmethod
    def generate_chunks(self, text: str) -> List[str]:
        pass
