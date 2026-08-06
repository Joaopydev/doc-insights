from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.presentation.interfaces.controller_interface import ControllerInterface

from src.chat.application.use_cases.websocket.connect import WebSocketConnectUseCase
from src.chat.application.use_cases.websocket.connect_dto import WebSocketConnectInput


class WebSocketConnectController(ControllerInterface):

    def __init__(self, use_case: WebSocketConnectUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:

        input_data = WebSocketConnectInput(
            user_id=request.user_id,
            connection_id=request.connection_id
        )
        self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=200,
            body={}
        )
