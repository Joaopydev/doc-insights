import pytest

from src.chat.domain.value_objects.message_type import MessageType
from src.chat.application.use_cases.ask_question.ask_question_dto import AskQuestionInput

from src.shared.domain.value_objects.document_status import DocumentStatus
from src.errors.types.document_not_found import DocumentNotFound
from src.errors.types.document_not_ready import DocumentNotReady
from src.errors.types.unauthorized_document_access import UnauthorizedDocumentAccess

from tests.unit.chat.factories import (
    create_ask_question_use_case,
    create_document,
    create_conversation,
)
from tests.unit.chat.mock_types import (
    ChatRepositoryMock,
    DocumentRepositoryMock,
    EventPublisherMock,
)


def test_ask_question_with_non_existent_document(
    chat_repository: ChatRepositoryMock,
    document_repository: DocumentRepositoryMock,
    event_publisher: EventPublisherMock,
):
    document_repository.get_document_by_id.return_value = None

    use_case = create_ask_question_use_case(
        chat_repository=chat_repository,
        document_repository=document_repository,
        event_publisher=event_publisher,
    )

    with pytest.raises(DocumentNotFound):
        use_case.execute(
            AskQuestionInput(
                user_id="",
                document_id="",
                question=""
            )
        )

def test_ask_question_with_invalid_document_status(
    chat_repository: ChatRepositoryMock,
    document_repository: DocumentRepositoryMock,
    event_publisher: EventPublisherMock,
):
    document = create_document(
        user_id="test-user-id",
        filename="document.pdf",
        content_type="application/pdf",
        document_status=DocumentStatus.INDEXING,
    )

    document_repository.get_document_by_id.return_value = document

    use_case = create_ask_question_use_case(
        chat_repository=chat_repository,
        document_repository=document_repository,
        event_publisher=event_publisher,
    )

    with pytest.raises(DocumentNotReady):
        use_case.execute(
            AskQuestionInput(
                user_id=document.user_id,
                document_id=document.id,
                question="",
            )
        )

    document_repository.get_document_by_id.assert_called_once_with(document.id)

def test_ask_question_with_unauthorized_document_accesss(
    chat_repository: ChatRepositoryMock,
    document_repository: DocumentRepositoryMock,
    event_publisher: EventPublisherMock,
):
    document = create_document(
        user_id="test-user-id",
        filename="document.pdf",
        content_type="application/pdf",
        document_status=DocumentStatus.READY,
    )
    document_repository.get_document_by_id.return_value = document

    use_case = create_ask_question_use_case(
        chat_repository=chat_repository,
        document_repository=document_repository,
        event_publisher=event_publisher,
    )

    with pytest.raises(UnauthorizedDocumentAccess):
        use_case.execute(
            AskQuestionInput(
                user_id="test-user-id-2",
                document_id=document.id,
                question="",
            )
        )

    document_repository.get_document_by_id.assert_called_once_with(document.id)

def test_ask_question_with_existent_conversation(
    chat_repository: ChatRepositoryMock,
    document_repository: DocumentRepositoryMock,
    event_publisher: EventPublisherMock,
):
    document = create_document(
        user_id="test-user-id",
        filename="document.pdf",
        content_type="application/pdf",
        document_status=DocumentStatus.READY,
    )
    document_repository.get_document_by_id.return_value = document

    conversation = create_conversation(
        document_id=document.id,
        user_id=document.user_id,
    )
    chat_repository.get_conversation_by_document_id.return_value = conversation

    use_case = create_ask_question_use_case(
        chat_repository=chat_repository,
        document_repository=document_repository,
        event_publisher=event_publisher,
    )

    question_input = AskQuestionInput(
            user_id=document.user_id,
            document_id=document.id,
            question="Will the flow pass?"
        )
    output = use_case.execute(question_input)

    saved_message = chat_repository.save_message.call_args.args[0]

    assert output.message_id == saved_message.id
    assert output.conversation_id == conversation.id

    chat_repository.save_conversation.assert_not_called()
    chat_repository.save_message.assert_called_once()
    chat_repository.get_conversation_by_document_id.assert_called_once_with(question_input.document_id)

    assert saved_message.conversation_id == conversation.id
    assert saved_message.content == question_input.question
    assert saved_message.message_type == MessageType.QUESTION

    event_publisher.publish.assert_called_once()

    saved_event = event_publisher.publish.call_args.args[0]

    assert saved_event.message_id == saved_message.id
    assert saved_event.document_id == document.id

def test_ask_question_with_non_existent_conversation(
    chat_repository: ChatRepositoryMock,
    document_repository: DocumentRepositoryMock,
    event_publisher: EventPublisherMock,
):
    document = create_document(
        user_id="test-user-id",
        filename="document.pdf",
        content_type="application/pdf",
        document_status=DocumentStatus.READY,
    )
    document_repository.get_document_by_id.return_value = document
    chat_repository.get_conversation_by_document_id.return_value = None

    use_case = create_ask_question_use_case(
        chat_repository=chat_repository,
        document_repository=document_repository,
        event_publisher=event_publisher,
    )

    question_input = AskQuestionInput(
            user_id=document.user_id,
            document_id=document.id,
            question="Will the flow pass?"
        )
    output = use_case.execute(question_input)

    saved_message = chat_repository.save_message.call_args.args[0]
    saved_conversation = chat_repository.save_conversation.call_args.args[0]

    assert output.message_id == saved_message.id
    assert output.conversation_id == saved_conversation.id

    chat_repository.get_conversation_by_document_id.assert_called_once_with(question_input.document_id)
    chat_repository.save_conversation.assert_called_once()

    assert saved_conversation.document_id == document.id
    assert saved_conversation.user_id == document.user_id

    chat_repository.save_message.assert_called_once()

    assert saved_message.conversation_id == saved_conversation.id
    assert saved_message.content == question_input.question
    assert saved_message.message_type == MessageType.QUESTION

    event_publisher.publish.assert_called_once()

    saved_event = event_publisher.publish.call_args.args[0]

    assert saved_event.message_id == saved_message.id
    assert saved_event.document_id == document.id
