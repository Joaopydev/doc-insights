from openai import AsyncOpenAI

from src.shared.application.ports.ai_client import AIClient as AIClientInterface


client = AsyncOpenAI()


class OpenAIClient(AIClientInterface):

    async def embedings_create(self, chunks: list[str]) -> list[float]:
        response = await client.embeddings.create(
            model="text-embedding-3-large",
            input=chunks
        )
        return [item.embedding for item in response.data]
