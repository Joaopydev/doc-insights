import json
import asyncio
from typing import Dict, Any

from src.main.composers.process_question_composer import ProcessQuestionComposer
from src.chat.application.use_cases.question_processing.process_question_dto import ProcessQuestionInput


async def async_handler(event: Dict[str, Any], context: Any):
    compose = ProcessQuestionComposer.compose()
    tasks = [
        compose(
            ProcessQuestionInput(
                message_id=json.dumps(record["body"]["message_id"]),
                document_id=json.dumps(record["body"]["document_id"]),
                cache_key=json.dumps(record["body"]["cache_key"]),
            )
        )
        for record in event["Records"]
    ]
    await asyncio.gather(**tasks)

def handler(event: Dict[str, Any], context: Any):
    asyncio.run(async_handler(event, context))
