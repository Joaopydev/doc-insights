from pydantic import BaseModel


class UpdateCacheInput(BaseModel):
    cache_key: str
    generated_response: str
