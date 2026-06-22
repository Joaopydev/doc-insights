from abc import ABC, abstractmethod
from src.shared.domain.entities.document import Document


class DocumentRepository(ABC):

    @abstractmethod
    def insert_document(self, document: Document) -> None:
        pass
