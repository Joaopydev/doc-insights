from abc import ABC, abstractmethod
from src.upload.domain.entities.document import Document


class DocumentRepository(ABC):

    @abstractmethod
    def save(self, document: Document) -> None:
        pass
