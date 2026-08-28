# pylint: disable=redefined-outer-name
from typing import cast, Dict
from unittest.mock import create_autospec, Mock

import pytest

from src.chat.application.use_cases.ask_question.ask_question import AskQuestionUseCase
from src.chat.application.use_cases.question_processing.question_processing_started import QuestionProcessingUseCase

from src.chat.application.ports.response_cache import ResponseCache
from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.application.ports.document_repository import DocumentRepository
from src.shared.application.ports.event_publisher import EventPublisher
from src.shared.application.ports.message_publisher import MessagePublisher

from tests.unit.chat.mock_types import (
    ChatRepositoryMock,
    DocumentRepositoryMock,
    EventPublisherMock,
    MessagePublisherMock,
    ResponseCacheMock,
)


@pytest.fixture
def mock_repositories() -> Dict[str, Mock]:
    return {
        "chat_repository": cast(
            ChatRepositoryMock,
            create_autospec(ChatRepository, instance=True)
        ),
        "document_repository": cast(
            DocumentRepositoryMock,
            create_autospec(DocumentRepository, instance=True)
        ),
        "event_publisher": cast(
            EventPublisherMock,
            create_autospec(EventPublisher, instance=True)
        ),
        "message_publisher": cast(
            MessagePublisherMock,
            create_autospec(MessagePublisher, instance=True)
        ),
        "response_cache": cast(
            ResponseCacheMock,
            create_autospec(ResponseCache, instance=True)
        ),
    }

@pytest.fixture
def ask_question_use_case(mock_repositories) -> AskQuestionUseCase:
    return AskQuestionUseCase(
        chat_repository=mock_repositories["chat_repository"],
        document_repository=mock_repositories["document_repository"],
        event_publisher=mock_repositories["event_publisher"],
    )

@pytest.fixture
def question_processing_use_case(mock_repositories) -> QuestionProcessingUseCase:
    return QuestionProcessingUseCase(
        chat_repository=mock_repositories["chat_repository"],
        event_publisher=mock_repositories["event_publisher"],
        response_cache=mock_repositories["response_cache"],
        message_publisher=mock_repositories["message_publisher"],
    )
