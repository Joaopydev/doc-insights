from typing import cast
from unittest.mock import create_autospec

import pytest

from src.chat.application.ports.chat_repository import ChatRepository
from src.chat.application.ports.document_repository import DocumentRepository
from src.shared.application.ports.event_publisher import EventPublisher

from tests.unit.chat.mock_types import (
    ChatRepositoryMock,
    DocumentRepositoryMock,
    EventPublisherMock,
)


@pytest.fixture
def chat_repository() -> ChatRepositoryMock:
    return cast(
        ChatRepositoryMock,
        create_autospec(ChatRepository, instance=True),
    )


@pytest.fixture
def document_repository() -> DocumentRepositoryMock:
    return cast(
        DocumentRepositoryMock,
        create_autospec(DocumentRepository, instance=True),
    )


@pytest.fixture
def event_publisher() -> EventPublisherMock:
    return cast(
        EventPublisherMock,
        create_autospec(EventPublisher, instance=True),
    )
