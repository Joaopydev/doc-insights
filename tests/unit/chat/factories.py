from src.shared.domain.entities.document import Document
from src.chat.domain.entities.conversation import Conversation

from src.chat.application.use_cases.ask_question.ask_question import AskQuestionUseCase
from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.application.ports.document_repository import DocumentRepository
from src.shared.application.ports.event_publisher import EventPublisher


def create_document(user_id: str, filename: str, content_type: str):
    return Document.create(
        user_id=user_id,
        metadata={
            "filename": filename,
            "content_type": content_type,
        }
    )

def create_conversation(document_id: str, user_id: str):
    return Conversation.create(
        document_id=document_id,
        user_id=user_id,
    )

def create_ask_question_use_case(
    chat_repository: ChatRepository,
    document_repository: DocumentRepository,
    event_publisher: EventPublisher,
):
    return AskQuestionUseCase(
        chat_repository=chat_repository,
        document_repository=document_repository,
        event_publisher=event_publisher,
    )
