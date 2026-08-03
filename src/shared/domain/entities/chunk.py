from datetime import datetime, UTC
from dataclasses import dataclass
from uuid import uuid4
from typing import List


@dataclass
class DocumentChunk:
    id: str
    document_id: str
    chunk_order: int
    content: str
    embedding: List[float]
    created_at: datetime

    @classmethod
    def create(
        cls,
        document_id: str,
        chunk_order: int,
        content: str,
        embedding: List[float],
    ):
        chunk_id = str(uuid4())
        now = datetime.now(UTC)

        return cls(
            id=chunk_id,
            document_id=document_id,
            chunk_order=chunk_order,
            content=content,
            embedding=embedding,
            created_at=now
        )

    @classmethod
    def restore(
        cls,
        chunk_id: str,
        document_id: str,
        chunk_order: int,
        content: str,
        embedding: List[float],
        created_at: datetime,
    ):
        return cls(
            id=chunk_id,
            document_id=document_id,
            chunk_order=chunk_order,
            content=content,
            embedding=embedding,
            created_at=created_at
        )
