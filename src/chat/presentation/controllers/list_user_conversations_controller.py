from src.chat.application.use_cases.list_conversations.list_user_conversations import ListUserConversationsUseCase

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.presentation.interfaces.controller_interface import ControllerInterface


class ListUserConversationsController(ControllerInterface):

    def __init__(self, use_case: ListUserConversationsUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        output = self.use_case.execute(user_id=request.user_id)

        return HTTPResponse(
            status_code=200,
            body={
                "conversations": [conv.to_dict() for conv in (output.conversations or [])]
            }
        )
