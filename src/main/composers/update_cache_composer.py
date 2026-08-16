from typing import Callable

from src.chat.application.use_cases.cache.update_cache import UpdateCacheUseCase
from src.chat.infrastructure.cache.redis_response_cache import RedisResponseCache


class UpdateCacheComposer:

    @staticmethod
    def compose() -> Callable:
        response_cache = RedisResponseCache()
        use_case = UpdateCacheUseCase(response_cache)
        return use_case.execute
