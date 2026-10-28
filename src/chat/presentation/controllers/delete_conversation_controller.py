from src.chat.application.use_cases.delete_conversation.delete_conversation_dto import DeleteConversationInput
from src.chat.application.use_cases.delete_conversation.delete_conversation import DeleteConversationUseCase

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.presentation.interfaces.controller_interface import ControllerInterface


class DeleteConversationController(ControllerInterface):

    def __init__(self, use_case: DeleteConversationUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = DeleteConversationInput(
            user_id=request.user_id,
            conversation_id=request.params["conversation_id"]
        )

        self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=200,
            body={}
        )
