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

    @abstractmethod
    def read_object_content(
        self,
        key: str,
    ) -> bytes:
        pass

    @abstractmethod
    def put_object(
        self, key: str,
        body: any,
        content_type: str
    ) -> None:
        pass
