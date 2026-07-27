from src.chat.application.use_cases.ask_question.ask_question_dto import (
    AskQuestionInput,
    AskQuestionOutput,
)
from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.domain.entities.chat_message import ChatMessage
from src.chat.application.events.question_asked_event import QuestionAskedEvent

from src.shared.application.ports.event_publisher import EventPublisher


class AskQuestionUseCase:

    def __init__(
        self,
        chat_repository: ChatRepository,
        event_publisher: EventPublisher,
    ):
        self.chat_repository = chat_repository
        self.event_publisher = event_publisher

    def execute(
        self,
        question_input: AskQuestionInput,
    ) -> AskQuestionOutput:

        message = ChatMessage.create(
            document_id=question_input.document_id,
            conversation_id=question_input.conversation_id,
            user_id=question_input.user_id,
            content=question_input.question,
        )

        self.chat_repository.save_message(message)

        self.event_publisher.publish(
            QuestionAskedEvent(
                message_id=message.id,
            )
        )

        return AskQuestionOutput(
            message_id=message.id,
            conversation_id=message.conversation_id,
        )
