from src.chat.application.ports.response_cache import ResponseCache
from src.chat.application.use_cases.cache.update_cache_dto import UpdateCacheInput


class UpdateCacheUseCase:

    def __init__(
        self,
        response_cache: ResponseCache,
    ) -> None:
        self.response_cache = response_cache

    def execute(
        self,
        input_dto: UpdateCacheInput,
    ) -> None:

        self.response_cache.set(
            key=input_dto.cache_key,
            value=input_dto.generated_response,
            ttl=3600,
        )
