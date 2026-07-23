from src.chat.application.use_cases.ask_question import AskQuestionUseCase
from src.chat.application.use_cases.ask_question_dto import AskQuestionInput

from src.shared.presentation.http_types.http_request import HTTPRequest
from src.shared.presentation.http_types.http_response import HTTPResponse
from src.shared.presentation.interfaces.controller_interface import ControllerInterface


class QuestionController(ControllerInterface):

    def __init__(self, use_case: AskQuestionUseCase) -> None:
        self.use_case = use_case

    def handle(self, request: HTTPRequest) -> HTTPResponse:
        input_data = AskQuestionInput(
            user_id=request.user_id,
            document_id=request.body["document_id"],
            question=request.body["question"]
        )

        output = self.use_case.execute(input_data)

        return HTTPResponse(
            status_code=202,
            body={
                "message_id": output.message_id,
                "conversation_id": output.conversation_id
            }
        )
