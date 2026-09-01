import pytest

from src.errors.types.conversation_not_found import ConversationNotFound
from src.chat.domain.value_objects.message_type import MessageType
from src.chat.application.use_cases.get_messages.get_messsages_dto import (
    GetMessagesInput,
    GetMessagesOutPut,
)

from tests.unit.chat.factories import (
    create_conversation,
    create_message,
)



def test_execute_should_return_conversation_not_found_when_conversation_does_not_exists(get_messages_use_case):
    get_messages_use_case.chat_repository.get_conversation_by_id.return_valeu = None

    input_dto = GetMessagesInput(
        user_id="test-user-id",
        conversation_id="test-conversation-id",
    )

    with pytest.raises(ConversationNotFound):
        get_messages_use_case.execute(input_dto)

    get_messages_use_case.chat_repository.get_conversation_by_id.assert_called_once()

def test_execute_should_return_conversation_not_found_if_user_is_not_the_owner(get_messages_use_case):
    conversation = create_conversation(
        document_id="test-document-id",
        user_id="test-user-id-1",
    )
    get_messages_use_case.chat_repository.get_conversation_by_id.return_valeu = conversation

    input_dto = GetMessagesInput(
        user_id="test-user-id-2",
        conversation_id=conversation.id,
    )

    with pytest.raises(ConversationNotFound):
        get_messages_use_case.execute(input_dto)

    get_messages_use_case.chat_repository.get_conversation_by_id.assert_called_once_with(conversation.id)


def test_execute_should_return_succesfully_when_conversation_exists(get_messages_use_case):
    conversation = create_conversation(
        document_id="test-document-id",
        user_id="test-user-id-1",
    )
    get_messages_use_case.chat_repository.get_conversation_by_id.return_value = conversation
    get_messages_use_case.chat_repository.get_messages.return_value = [
        create_message(
            conversation_id=conversation.id,
            content="Will the flow pass?",
            message_type=MessageType.QUESTION
        ),
        create_message(
            conversation_id=conversation.id,
            content="Yes, the flow should pass",
            message_type=MessageType.ANSWER
        ),
    ]

    input_dto = GetMessagesInput(
        user_id=conversation.user_id,
        conversation_id=conversation.id,
    )

    messages = get_messages_use_case.execute(input_dto)

    get_messages_use_case.chat_repository.get_conversation_by_id.assert_called_once_with(conversation.id)
    get_messages_use_case.chat_repository.get_messages.assert_called_once_with(conversation.id)

    assert isinstance(messages, GetMessagesOutPut)
