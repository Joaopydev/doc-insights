from abc import ABC, abstractmethod


class GatewayClient(ABC):

    @abstractmethod
    def get_connection(
        self,
        connection_id: str
    ) -> None:
        pass

    @abstractmethod
    def post_to_connection(
        self,
        connection_id: str,
        data: dict,
    ) -> None:
        pass
