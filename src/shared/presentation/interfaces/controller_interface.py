from abc import ABC, abstractmethod

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse



class ControllerInterface(ABC):

    @abstractmethod
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        pass
