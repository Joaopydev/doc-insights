import pytest

from src.chat.domain.value_objects.message_type import MessageType
from src.chat.application.events.question_asked_event import QuestionAskedEvent

from tests.unit.chat.factories import (
    create_message,
)


@pytest.mark.asyncio
async def test_execute_should_return_early_when_message_not_found(question_processing_use_case):
    event = QuestionAskedEvent(
        message_id="test-message-id",
        document_id="test-document-id",
    )
    question_processing_use_case.chat_repository.get_message_by_id.return_value = None

    await question_processing_use_case.execute(event)

    question_processing_use_case.chat_repository.get_message_by_id.assert_called_once_with(event.message_id)
    question_processing_use_case.response_cache.create_cache_key.assert_not_called()

@pytest.mark.asyncio
async def test_execute_should_publish_message_when_cache_miss(question_processing_use_case):
    message = create_message(
        conversation_id="test-conversation-id",
        content="Will the flow pass?",
        message_type=MessageType.QUESTION
    )

    event = QuestionAskedEvent(
        message_id=message.id,
        document_id="test-document-id",
    )

    question_processing_use_case.chat_repository.get_message_by_id.return_value = message
    question_processing_use_case.response_cache.create_cache_key.return_value = "test-cache-key"
    question_processing_use_case.response_cache.get.return_value = None

    await question_processing_use_case.execute(event)

    question_processing_use_case.chat_repository.get_message_by_id.assert_called_once_with(message.id)
    question_processing_use_case.response_cache.create_cache_key.assert_called_once_with(
        document_id=event.document_id,
        question=message.content,
    )
    question_processing_use_case.response_cache.get.assert_called_once_with(
        question_processing_use_case.response_cache.create_cache_key.return_value
    )
    question_processing_use_case.message_publisher.send_message.assert_called_once_with(
        {
            "message_id": message.id,
            "document_id": event.document_id,
            "cache_key": question_processing_use_case.response_cache.create_cache_key.return_value,
        }
    )
    question_processing_use_case.chat_repository.save_message.assert_not_called()
    question_processing_use_case.event_publisher.publish.assert_not_called()

@pytest.mark.asyncio
async def test_execute_should_save_message_and_publish_event_when_cache_hit(question_processing_use_case):
    message = create_message(
        conversation_id="test-conversation-id",
        content="Will the flow pass?",
        message_type=MessageType.QUESTION
    )

    event = QuestionAskedEvent(
        message_id=message.id,
        document_id="test-document-id",
    )

    question_processing_use_case.chat_repository.get_message_by_id.return_value = message
    question_processing_use_case.response_cache.create_cache_key.return_value = "test-cache-key"
    question_processing_use_case.response_cache.get.return_value = "Yes, the text flow should pass."

    await question_processing_use_case.execute(event)

    question_processing_use_case.chat_repository.get_message_by_id.assert_called_once_with(message.id)
    question_processing_use_case.response_cache.create_cache_key.assert_called_once_with(
        document_id=event.document_id,
        question=message.content,
    )
    question_processing_use_case.response_cache.get.assert_called_once_with(
        question_processing_use_case.response_cache.create_cache_key.return_value
    )
    question_processing_use_case.message_publisher.send_message.assert_not_called()
    question_processing_use_case.chat_repository.save_message.assert_called_once()
    question_processing_use_case.event_publisher.publish.assert_called_once()

    saved_event = question_processing_use_case.event_publisher.publish.call_args.args[0]

    assert saved_event.conversation_id == message.conversation_id
