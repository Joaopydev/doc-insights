from src.chat.application.ports.response_cache import ResponseCache
from src.chat.application.events.update_cache_event import UpdateCacheEvent


class UpdateCacheUseCase:

    def __init__(
        self,
        response_cache: ResponseCache,
    ) -> None:
        self.response_cache = response_cache

    def execute(
        self,
        event: UpdateCacheEvent,
    ) -> None:

        self.response_cache.set(
            key=event.cache_key,
            value=event.generated_response,
            ttl=3600,
        )
