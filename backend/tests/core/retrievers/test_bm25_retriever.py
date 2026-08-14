import pytest

from ai_assistant.core.models import Chunk, RetrievalOptions
from ai_assistant.core.retrievers import BM25Retriever


@pytest.fixture
def chunks():
    return [
        Chunk(
            content="FastAPI is a modern Python web framework.",
        ),
        Chunk(
            content="PostgreSQL is a relational database system.",
        ),
        Chunk(
            content="Redis is an in-memory data store.",
        ),
    ]


@pytest.fixture
def retriever(chunks):
    retriever = BM25Retriever()

    retriever.build_index(chunks)

    return retriever


def test_retriever_returns_matching_chunk(retriever):
    results = retriever.retrieve("FastAPI")

    assert len(results) > 0
    assert results[0].content == (
        "FastAPI is a modern Python web framework."
    )


def test_retriever_respects_top_k(retriever):
    results = retriever.retrieve(
        "database",
        options=RetrievalOptions(top_k=2),
    )

    assert len(results) == 2


def test_retriever_uses_default_options(retriever):
    results = retriever.retrieve("FastAPI")

    assert len(results) == 3


def test_retriever_raises_error_before_index_is_built():
    retriever = BM25Retriever()

    with pytest.raises(
        ValueError,
        match="BM25 index has not been built.",
    ):
        retriever.retrieve("FastAPI")