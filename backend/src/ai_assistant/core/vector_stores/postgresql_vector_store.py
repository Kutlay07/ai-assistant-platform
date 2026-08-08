import psycopg
from pgvector.psycopg import register_vector

from ..models import Chunk
from .base_vector_store import BaseVectorStore


class PostgreSQLVectorStore(BaseVectorStore):

    def __init__(self, connection_string: str):
        self._connection = psycopg.connect(connection_string)
        register_vector(self._connection)

    def add(self, chunks: list[Chunk]) -> None:
        for chunk in chunks:
            if chunk.embedding is None:
                raise ValueError(
                    "Chunk must have an embedding before being added."
                )

        with self._connection.cursor() as cursor:
            for chunk in chunks:
                cursor.execute(
                    """
                    INSERT INTO chunks (content, embedding)
                    VALUES (%s, %s)
                    """,
                    (chunk.content, chunk.embedding),
                )

        self._connection.commit()

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[Chunk]:

        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT content
                FROM chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (embedding, top_k),
            )

            rows = cursor.fetchall()

        return [
            Chunk(content=row[0])
            for row in rows
        ]

    def close(self) -> None:
        self._connection.close()