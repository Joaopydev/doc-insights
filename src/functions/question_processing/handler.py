import asyncio
from typing import Dict, Any

from src.chat.application.events.question_asked_event import QuestionAskedEvent
from src.main.composers.question_processing_composer import QuestionProcessingComposer


async def async_handler(event: Dict[str, Any], context: Any):
    compose = QuestionProcessingComposer.compose()
    await compose(
        QuestionAskedEvent(
            message_id=event["detail"]["message_id"],
            document_id=event["detail"]["document_id"]
        )
    )

def handler(event: Dict[str, Any], context: Any):
    asyncio.run(async_handler(event, context))
