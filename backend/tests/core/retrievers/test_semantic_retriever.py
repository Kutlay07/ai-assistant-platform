from unittest.mock import MagicMock

from ai_assistant.core.models import Chunk
from ai_assistant.core.retrievers.semantic_retriever import SemanticRetriever


def test_retrieve_cache_miss():
    embedder = MagicMock()
    vector_store = MagicMock()
    cache = MagicMock()

    cache.get.return_value = None

    embedder.embed.return_value = [1.0, 2.0]

    chunks = [
        Chunk(content="chunk 1"),
        Chunk(content="chunk 2"),
    ]

    vector_store.search.return_value = chunks

    retriever = SemanticRetriever(
        embedder=embedder,
        vector_store=vector_store,
        cache=cache,
    )

    result = retriever.retrieve("hello")

    assert result == chunks

    embedder.embed.assert_called_once_with("hello")
    vector_store.search.assert_called_once()
    cache.set.assert_called_once()


def test_retrieve_cache_hit():
    embedder = MagicMock()
    vector_store = MagicMock()
    cache = MagicMock()

    cache.get.return_value = [
        {
            "content": "cached",
            "embedding": None,
            "document": None,
        }
    ]

    retriever = SemanticRetriever(
        embedder=embedder,
        vector_store=vector_store,
        cache=cache,
    )

    result = retriever.retrieve("hello")

    assert len(result) == 1
    assert result[0].content == "cached"

    embedder.embed.assert_not_called()
    vector_store.search.assert_not_called()
    cache.set.assert_not_called()


def test_retrieve_without_cache():
    embedder = MagicMock()
    vector_store = MagicMock()

    embedder.embed.return_value = [1.0]

    chunks = [
        Chunk(content="chunk"),
    ]

    vector_store.search.return_value = chunks

    retriever = SemanticRetriever(
        embedder=embedder,
        vector_store=vector_store,
    )

    result = retriever.retrieve("hello")

    assert result == chunks

    embedder.embed.assert_called_once()
    vector_store.search.assert_called_once()


"""
import pytest

from ai_assistant.core.embedders import SentenceTransformerEmbedder
from ai_assistant.core.models import Chunk
from ai_assistant.core.models import RetrievalOptions
from ai_assistant.core.retrievers import SemanticRetriever
from ai_assistant.core.vector_stores import PostgreSQLVectorStore


@pytest.fixture
def vector_store():
    store = PostgreSQLVectorStore(
        "postgresql://ai_assistant:ai_assistant@localhost:5432/ai_assistant"
    )

    with store._connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE chunks RESTART IDENTITY")

    store._connection.commit()

    yield store

    with store._connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE chunks RESTART IDENTITY")

    store._connection.commit()
    store.close()


def test_retriever_performs_semantic_search(vector_store):
    embedder = SentenceTransformerEmbedder()

    chunks = [
        Chunk(
            content="FastAPI is a modern Python web framework."
        ),
        Chunk(
            content="PostgreSQL is a relational database system."
        ),
        Chunk(
            content="Redis is an in-memory data store."
        ),
    ]

    for chunk in chunks:
        chunk.embedding = embedder.embed(chunk.content)

    vector_store.add(chunks)

    retriever = SemanticRetriever(
        embedder=embedder,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        "What is FastAPI?",
        options=RetrievalOptions(top_k=1),
    )

    assert len(results) == 1
    assert results[0].content == (
        "FastAPI is a modern Python web framework."
    )
"""