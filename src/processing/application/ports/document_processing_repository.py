from abc  import ABC, abstractmethod
from typing import Optional

from src.shared.domain.entities.document import Document


class DocumentProcessingRepository(ABC):

    @abstractmethod
    def get_document_by_storage_key(self, storage_key: str) -> Optional[Document]:
        pass

    @abstractmethod
    def update_status(self, document_id: str, status: str):
        pass

    @abstractmethod
    def update_textract_job_id(self, document_id: str, job_id: str):
        pass
