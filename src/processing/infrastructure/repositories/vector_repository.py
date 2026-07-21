# pylint: disable=no-member
from typing import List

from src.processing.application.ports.vector_repository import (
    VectorRepository as VectorRepositoryInterface
)
from src.processing.domain.entities.chunk  import DocumentChunk

from src.shared.infrastructure.neon.connection import VectorDatabaseConnection

class VectorRepository(VectorRepositoryInterface):

    def __init__(self):
        self.connection = VectorDatabaseConnection()

    def store_chunks(self, chunks: List[DocumentChunk]):
        with self.connection as conn:
            with conn.cursor() as cur:
                try:
                    for chunk in chunks:
                        cur.execute(
                            """
                            INSERT INTO document_chunks (
                                id,
                                document_id,
                                chunk_order,
                                content,
                                embedding,
                                created_at
                            )
                            VALUES (%s, %s, %s, %s, %s, %s)
                            """,
                            (
                                chunk.id,
                                chunk.document_id,
                                chunk.chunk_order,
                                chunk.content,
                                chunk.embedding,
                                chunk.created_at,
                            )
                        )
                except Exception as e:
                    print("Error storing chunks:", e)
                    raise
