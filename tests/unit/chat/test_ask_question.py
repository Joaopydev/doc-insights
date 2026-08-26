import pytest

from src.chat.application.use_cases.ask_question.ask_question_dto import AskQuestionInput
from src.errors.types.document_not_found import DocumentNotFound

from tests.unit.chat.factories import (
    create_ask_question_use_case
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
