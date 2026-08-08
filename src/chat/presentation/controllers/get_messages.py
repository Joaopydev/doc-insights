from src.chat.application.use_cases.get_messages.get_messsages_dto import GetMessagesInput
from src.chat.application.use_cases.get_messages.get_messages import GetMessagesUseCase

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.presentation.interfaces.controller_interface import ControllerInterface


class GetMessagesController(ControllerInterface):

    def __init__(self, use_case: GetMessagesUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = GetMessagesInput(
            user_id=request.user_id,
            conversation_id=request.params["conversation_id"]
        )

        output = self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=200,
            body={
                "messages": [message.to_dict() for message in output.messages]
            }
        )
