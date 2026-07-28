from enum import StrEnum


class MessageType(StrEnum):
    QUESTION: str = "QUESTION"
    ANSWER: str = "ANSWER"
