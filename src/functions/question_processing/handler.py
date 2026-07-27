import asyncio
from typing import Dict, Any
import traceback

from src.chat.application.events.question_asked_event import QuestionAskedEvent
from src.main.composers.question_processing_composer import QuestionProcessingComposer


async def async_handler(event: Dict[str, Any], context: Any):
    try:
        compose = QuestionProcessingComposer.compose()
        await compose(QuestionAskedEvent(event["detail"]["message_id"]))
    except Exception:
        traceback.print_exc()

def handler(event: Dict[str, Any], context: Any):
    asyncio.run(async_handler(event, context))
