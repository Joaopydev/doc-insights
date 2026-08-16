from abc import ABC, abstractmethod
from typing import Dict


class MessagePublisher(ABC):

    @abstractmethod
    def send_message(self, message_body: Dict[str, any]) -> None:
        pass
