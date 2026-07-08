from abc import ABC, abstractmethod
from typing import List


class EmbeddingGenerator(ABC):

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        pass
