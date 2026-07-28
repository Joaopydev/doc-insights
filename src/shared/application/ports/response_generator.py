from abc import ABC, abstractmethod


class ResponseGenerator(ABC):

    @abstractmethod
    async def generate(
        self,
        question: str,
        context: str,
    ) -> str:
        pass
