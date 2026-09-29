from typing import Dict, Any

from src.shared.application.events.create_conversation_event import CreateConversationEvent
from src.main.composers.create_conversation_composer import CreateConversationComposer


def handler(event: Dict[str, Any], context: Any) -> None:
    question_answered_event = CreateConversationEvent(
        user_id=event["detail"]["user_id"],
        document_id=event["detail"]["document_id"]
    )
    compose = CreateConversationComposer.compose()
    compose(question_answered_event)
