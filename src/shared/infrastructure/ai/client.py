from typing import List
from openai import AsyncOpenAI

from src.shared.application.ports.ai_client import AIClient as AIClientInterface


client = AsyncOpenAI()


class OpenAIClient(AIClientInterface):

    async def embeddings_create(self, chunks: List[str]) -> List[List[float]]:
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=chunks
        )
        return [item.embedding for item in response.data]
