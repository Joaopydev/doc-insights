from abc import ABC, abstractmethod
from typing import Optional

from src.shared.domain.entities.document import Document


class DocumentRepository(ABC):

    @abstractmethod
    def get_document_by_id(self, document_id: str) -> Optional[Document]:
        pass

    @abstractmethod
    def update_conversation_id(self, document_id: str, conversation_id: str) -> None:
        pass
