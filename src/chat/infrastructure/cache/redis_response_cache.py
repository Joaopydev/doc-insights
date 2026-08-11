import re
import hashlib
from typing import Optional
from unicodedata import normalize

import redis

from src.chat.application.ports.response_cache import ResponseCache
from src.main.config.settings import settings


class RedisResponseCache(ResponseCache):

    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=int(settings.redis_port),
            decode_responses=True,
        )

    def get(self, key: str) -> Optional[str]:
        return self.redis_client.get(key)

    def set(self, key: str, value: str, ttl: int) -> None:
        self.redis_client.set(
            name=key,
            value=value,
            ex=ttl,
        )

    def create_cache_key(
        self,
        document_id: str,
        question: str,
    ) -> str:

        question_clean = question.strip().lower()
        question_clean = re.sub(r"\s+", " ", question_clean)
        nfkd = normalize("NFKD", question_clean)
        normalized_question = re.sub(r"[\u0300-\u036f]", "", nfkd)
        normalized_question = re.sub(r"[^a-z0-9 ]", "", normalized_question)

        question_hash = hashlib.sha256(
            normalized_question.encode("utf-8")
        ).hexdigest()

        return f"{document_id}:{question_hash}"
