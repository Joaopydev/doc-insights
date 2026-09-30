from src.chat.application.use_cases.get_conversation.get_conversation_dto import GetConversationByIdInput
from src.chat.application.use_cases.get_conversation.get_conversation_by_id import GetConversationByIdUseCase

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.presentation.interfaces.controller_interface import ControllerInterface


class GetConversationByIdController(ControllerInterface):

    def __init__(self, use_case: GetConversationByIdUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = GetConversationByIdInput(
            user_id=request.user_id,
            conversation_id=request.params["conversation_id"]
        )

        output = self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=200,
            body={
                "conversation": output.conversation.to_dict()
            }
        )
