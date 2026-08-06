from abc import ABC, abstractmethod


class WebSocketService(ABC):

    @abstractmethod
    def post_to_connection(
        self,
        connection_id: str,
        data: dict
    ) -> None:
        pass
