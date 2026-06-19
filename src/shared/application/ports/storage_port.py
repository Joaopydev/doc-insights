from abc import ABC, abstractmethod


class StoragePort(ABC):

    @abstractmethod
    def generate_presigned_url(
        self,
        file_key: str,
        content_type: str,
        expire_in: int
    ) -> str:
        pass
