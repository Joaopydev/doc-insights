from abc import ABC, abstractmethod


class DBClient(ABC):

    @abstractmethod
    def save(self, table_name: str, item: dict):
        pass
