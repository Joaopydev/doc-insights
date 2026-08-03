# pylint: disable=no-member
from typing import List

from src.shared.application.ports.vector_repository import (
    VectorRepository as VectorRepositoryInterface
)
from src.shared.infrastructure.neon.connection import VectorDatabaseConnection

from src.shared.domain.entities.chunk  import DocumentChunk


class VectorRepository(VectorRepositoryInterface):

    def __init__(self):
        self.connection = VectorDatabaseConnection()

    def store_chunks(self, chunks: List[DocumentChunk]):
        with self.connection as conn:
            with conn.cursor() as cur:
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

    def semantic_similarity_search(
        self,
        embedding: List[float],
        document_id: str,
        limit: int = 5
    ) -> List[DocumentChunk]:

        with self.connection as conn:
            with conn.cursor() as cur:

                query_vector = "[" + ",".join(map(str, embedding)) + "]"

                cur.execute(
                    """
                    SELECT
                        id,
                        document_id,
                        chunk_order,
                        content,
                        embedding,
                        created_at,
                        embedding <=> %s::vector AS distance
                    FROM document_chunks
                    WHERE document_id = %s
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        query_vector,
                        document_id,
                        query_vector,
                        limit
                    )
                )

                rows = cur.fetchall()

                return [
                    DocumentChunk(
                        id=row[0],
                        document_id=row[1],
                        chunk_order=row[2],
                        content=row[3],
                        embedding=row[4],
                        created_at=row[5]
                    )
                    for row in rows
                ]
