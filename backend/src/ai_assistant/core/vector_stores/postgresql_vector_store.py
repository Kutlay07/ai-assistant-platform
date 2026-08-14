import psycopg
from pgvector.psycopg import register_vector

from ..models import Chunk
from .base_vector_store import BaseVectorStore


class PostgreSQLVectorStore(BaseVectorStore):

    def __init__(self, connection_string: str):
        self._connection = psycopg.connect(connection_string)

        self._initialize()

        register_vector(self._connection)

    def _initialize(self) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE EXTENSION IF NOT EXISTS vector;

                CREATE TABLE IF NOT EXISTS chunks (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    embedding vector(384) NOT NULL
                );
                """
            )

        self._connection.commit()

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

    def get_all_chunks(self) -> list[Chunk]:
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, content
                FROM chunks
                """
            )

            rows = cursor.fetchall()

        return [
            Chunk(
                chunk_id=row[0],
                content=row[1],
            )
            for row in rows
        ]

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[Chunk]:

        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, content
                FROM chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """,
                (embedding, top_k),
            )

            rows = cursor.fetchall()

        return [
            Chunk(
                chunk_id=row[0],
                content=row[1],
            )
            for row in rows
        ]

    def close(self) -> None:
        self._connection.close()