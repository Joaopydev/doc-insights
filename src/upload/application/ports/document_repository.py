from abc import ABC, abstractmethod
from src.upload.domain.entities.document import Document


class DocumentRepository(ABC):

    @abstractmethod
    def insert_document(self, document: Document) -> None:
        pass
