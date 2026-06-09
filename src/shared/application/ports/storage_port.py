from abc import ABC, abstractmethod


class StoragePort(ABC):

    @abstractmethod
    def get_presigned_url(
        self,
        document_key: str,
        content_type: str,
        expire_in: int
    ) -> str:
        pass
