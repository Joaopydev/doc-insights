from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.presentation.interfaces.controller_interface import ControllerInterface

from src.chat.application.use_cases.websocket.disconnect import WebSocketDisconnectUseCase
from src.chat.application.use_cases.websocket.disconnect_dto import WebSocketDisconnectInput


class WebSocketDisconnectController(ControllerInterface):

    def __init__(self, use_case: WebSocketDisconnectUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:

        input_data = WebSocketDisconnectInput(
            connection_id=request.connection_id
        )
        self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=200,
            body={}
        )
