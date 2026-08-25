import json
import asyncio
from typing import Dict, Any

from src.main.config.logger import logger
from src.main.composers.process_question_composer import ProcessQuestionComposer
from src.chat.application.use_cases.question_processing.process_question_dto import ProcessQuestionInput


def parse_record(record: Dict[str, Any]) -> ProcessQuestionInput:
    body = json.loads(record["body"])

    return ProcessQuestionInput(
        message_id=body["message_id"],
        document_id=body["document_id"],
        cache_key=body["cache_key"],
    )

async def async_handler(event: Dict[str, Any], context: Any):
    compose = ProcessQuestionComposer.compose()
    tasks = [
        compose(parse_record(record))
        for record in event["Records"]
    ]
    await asyncio.gather(*tasks)

@logger.inject_lambda_context
def handler(event: Dict[str, Any], context: Any):
    asyncio.run(async_handler(event, context))
