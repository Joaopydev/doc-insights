from abc import ABC, abstractmethod


class TextExtractor(ABC):

    @abstractmethod
    def extract(self, file_bytes: bytes) -> str:
        pass
