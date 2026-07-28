from src.shared.application.ports.response_generator import (
    ResponseGenerator as ResponseGeneratorInterface
)
from src.shared.application.ports.ai_client import AIClient


class ResponseGenerator(ResponseGeneratorInterface):

    def __init__(
        self,
        ai_client: AIClient
    ):
        self.ai_client = ai_client

    async def generate(
        self,
        question: str,
        context: str,
    ):
        return await self.ai_client.generate_response(
            question=question,
            context=context,
        )
