from abc import ABC, abstractmethod
from src.shared.domain.entities.document import Document


class DocumentRepository(ABC):

    @abstractmethod
    def insert_document(self, document: Document) -> None:
        pass

    @abstractmethod
    def get_document_by_id(self, document_id: str) -> Document:
        pass

    @abstractmethod
    def delete_document_by_id(self, document_id: str) -> None:
        pass
