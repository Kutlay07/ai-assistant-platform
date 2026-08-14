from unittest.mock import MagicMock, patch

import pytest

from ai_assistant.core.models import Chunk
from ai_assistant.core.vector_stores import PostgreSQLVectorStore


CONNECTION_STRING = "postgresql://test:test@localhost:5432/test"


@patch("ai_assistant.core.vector_stores.postgresql_vector_store.register_vector")
@patch("ai_assistant.core.vector_stores.postgresql_vector_store.psycopg.connect")
def test_add_inserts_embedded_chunks(mock_connect, mock_register_vector):
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    mock_connect.return_value = connection

    store = PostgreSQLVectorStore(CONNECTION_STRING)
    cursor.reset_mock()
    connection.commit.reset_mock()

    chunk = Chunk(
        content="Hello world",
        embedding=[0.1, 0.2, 0.3],
    )

    store.add([chunk])

    cursor.execute.assert_called_once()
    connection.commit.assert_called_once()


@patch("ai_assistant.core.vector_stores.postgresql_vector_store.register_vector")
@patch("ai_assistant.core.vector_stores.postgresql_vector_store.psycopg.connect")
def test_add_rejects_chunk_without_embedding(mock_connect, mock_register_vector):
    connection = MagicMock()
    mock_connect.return_value = connection

    store = PostgreSQLVectorStore(CONNECTION_STRING)
    connection.commit.reset_mock()

    chunk = Chunk(
        content="Hello world",
        embedding=None,
    )

    with pytest.raises(ValueError, match="embedding"):
        store.add([chunk])

    connection.commit.assert_not_called()


@patch("ai_assistant.core.vector_stores.postgresql_vector_store.register_vector")
@patch("ai_assistant.core.vector_stores.postgresql_vector_store.psycopg.connect")
def test_search_returns_chunks(mock_connect, mock_register_vector):
    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [
        (1, "First result",),
        (2, "Second result",),
    ]
    mock_connect.return_value = connection

    store = PostgreSQLVectorStore(CONNECTION_STRING)
    cursor.reset_mock()

    results = store.search(
        embedding=[0.1, 0.2, 0.3],
        top_k=2,
    )

    assert len(results) == 2
    assert results[0].content == "First result"
    assert results[1].content == "Second result"

    cursor.execute.assert_called_once()