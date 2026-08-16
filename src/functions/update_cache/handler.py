from typing import Dict, Any

from src.chat.application.use_cases.cache.update_cache_dto import UpdateCacheInput
from src.main.composers.update_cache_composer import UpdateCacheComposer


def handler(event: Dict[str, Any], context: Any):

    compose = UpdateCacheComposer.compose()
    compose(
        UpdateCacheInput(
            cache_key=event["detail"]["cache_key"],
            generated_response=event["detail"]["generated_response"]
        )
    )
