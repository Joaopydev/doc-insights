from typing import List
from openai import AsyncOpenAI

from src.shared.application.ports.ai_client import AIClient
from src.shared.application.prompts.question_answer_prompt import QuestionAnswerPrompt


class OpenAIClient(AIClient):

    def __init__(self) -> None:
        self.client = AsyncOpenAI()

    async def create_embeddings(self, chunks: List[str]) -> List[List[float]]:
        response = await self.client.embeddings.create(
            model="text-embedding-3-small",
            input=chunks
        )
        return [item.embedding for item in response.data]

    async def generate_response(
        self,
        question: str,
        context: str,
    ):
        reponse = await self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": QuestionAnswerPrompt.build(context),
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return reponse.choices[0].message.content
