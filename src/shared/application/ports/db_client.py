from abc import ABC, abstractmethod


class DBClient(ABC):

    @abstractmethod
    def save(self, table_name: str, item: dict):
        pass

    @abstractmethod
    def get_item(self, table_name: str, key: dict):
        pass

    @abstractmethod
    def query(self, table_name: str, index_name: str, key_name: str, key_value: str):
        pass
