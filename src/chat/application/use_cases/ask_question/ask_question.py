from src.chat.application.use_cases.ask_question.ask_question_dto import (
    AskQuestionInput,
    AskQuestionOutput,
)
from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.domain.entities.chat_message import ChatMessage
from src.chat.domain.entities.conversation import Conversation
from src.chat.application.events.question_asked_event import QuestionAskedEvent
from src.chat.application.ports.document_repository import DocumentRepository

from src.errors.types.document_not_found import DocumentNotFound
from src.errors.types.unauthorized_document_access import UnauthorizedDocumentAccess


from src.shared.application.ports.event_publisher import EventPublisher

class AskQuestionUseCase:

    def __init__(
        self,
        chat_repository: ChatRepository,
        document_repository: DocumentRepository,
        event_publisher: EventPublisher,
    ):
        self.chat_repository = chat_repository
        self.document_repository = document_repository
        self.event_publisher = event_publisher

    def execute(
        self,
        question_input: AskQuestionInput,
    ) -> AskQuestionOutput:

        document = self.document_repository.get_document_by_id(question_input.document_id)
        if not document:
            raise DocumentNotFound("Document not found.")

        if question_input.user_id != document.user_id:
            raise UnauthorizedDocumentAccess("The current user is not the owner of the document")

        conversation = self.chat_repository.get_conversation_by_document_id(question_input.document_id)
        if not conversation:
            conversation = Conversation.create(
                document_id=question_input.document_id,
                user_id=question_input.user_id
            )
            self.chat_repository.save_conversation(conversation)

        message = ChatMessage.create(
            conversation_id=conversation.id,
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
