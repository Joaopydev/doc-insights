from typing import Dict, Any

from src.chat.application.events.update_cache_event import UpdateCacheEvent
from src.main.composers.update_cache_composer import UpdateCacheComposer
from src.main.config.logger import logger


@logger.inject_lambda_context
def handler(event: Dict[str, Any], context: Any):

    compose = UpdateCacheComposer.compose()
    compose(
        UpdateCacheEvent(
            cache_key=event["detail"]["cache_key"],
            generated_response=event["detail"]["generated_response"]
        )
    )
