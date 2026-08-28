from unittest.mock import call
import pytest


from src.chat.domain.value_objects.message_type import MessageType
from src.chat.application.use_cases.question_processing.process_question_dto import ProcessQuestionInput

from src.chat.application.events.question_answered_event import QuestionAnsweredEvent
from src.chat.application.events.update_cache_event import UpdateCacheEvent

from tests.unit.chat.factories import (
    create_message,
    create_document_chunk,
)

@pytest.mark.asyncio
async def test_execute_should_return_early_when_message_not_found(process_question_use_case):
    input_dto = ProcessQuestionInput(
        message_id="test-message-id",
        document_id="test-document-id",
        cache_key="test-cache-key"
    )

    process_question_use_case.chat_repository.get_message_by_id.return_value = None
    await process_question_use_case.execute(input_dto)

    process_question_use_case.embedding_generator.generate_embedding.assert_not_called()

@pytest.mark.asyncio
async def test_execute_should_process_question_succesfully_when_message_exists(process_question_use_case):
    message = create_message(
        conversation_id="test-conversation-id",
        content="Will the flow pass?",
        message_type=MessageType.QUESTION
    )

    input_dto = ProcessQuestionInput(
        message_id=message.id,
        document_id="test-document-id",
        cache_key="test-cache-key"
    )

    process_question_use_case.chat_repository.get_message_by_id.return_value = message
    process_question_use_case.embedding_generator.generate_embedding.return_value = [[0.1, 0.2, 0.3, 0.4]]
    process_question_use_case.vector_repository.semantic_similarity_search.return_value = [
        create_document_chunk(
            document_id=input_dto.document_id,
            chunk_order=1,
            content="First relevant text",
            embedding=[0.1, 0.2, 0.3, 0.4],
        ),
        create_document_chunk(
            document_id=input_dto.document_id,
            chunk_order=2,
            content="Second relevant text",
            embedding=[0.1, 0.2, 0.3, 0.4],
        )
    ]
    process_question_use_case.response_generator.generate.return_value = "Yes, the test flow should pass."

    await process_question_use_case.execute(input_dto)

    process_question_use_case.embedding_generator.generate_embedding.assert_called_once_with([message.content])
    process_question_use_case.vector_repository.semantic_similarity_search.assert_called_once_with(
        embedding=process_question_use_case.embedding_generator.generate_embedding.return_value[0],
        document_id=input_dto.document_id,
    )
    process_question_use_case.response_generator.generate.assert_called_once()
    process_question_use_case.chat_repository.save_message.assert_called_once()
    process_question_use_case.event_publisher.publish.assert_has_calls(
        [
            call(
                QuestionAnsweredEvent(
                    conversation_id=message.conversation_id
                )
            ),
            call(
                UpdateCacheEvent(
                    cache_key=input_dto.cache_key,
                    generated_response=process_question_use_case.response_generator.generate.return_value,
                )
            ),
        ]
    )

    assert process_question_use_case.event_publisher.publish.call_count == 2

    calls = process_question_use_case.event_publisher.publish.call_args_list

    assert len(calls) == 2

    question_answered_event = calls[0].args[0]
    update_cache_event = calls[1].args[0]

    assert isinstance(question_answered_event, QuestionAnsweredEvent)
    assert question_answered_event.conversation_id == message.conversation_id

    assert isinstance(update_cache_event, UpdateCacheEvent)
    assert update_cache_event.cache_key == input_dto.cache_key
    assert update_cache_event.generated_response == process_question_use_case.response_generator.generate.return_value
