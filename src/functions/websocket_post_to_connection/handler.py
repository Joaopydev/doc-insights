from typing import Dict, Any

from src.chat.application.events.question_answered_event import QuestionAnsweredEvent
from src.main.composers.websocket_post_to_connection_composer import WebSocketPostToConnectionComposer


def handler(event: Dict[str, Any], context: Any) -> None:
    question_answered_event = QuestionAnsweredEvent(
        conversation_id=event["detail"]["conversation_id"]
    )
    compose = WebSocketPostToConnectionComposer.compose()
    compose(question_answered_event)
