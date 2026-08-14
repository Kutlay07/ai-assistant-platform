from unittest.mock import MagicMock

from ai_assistant.core.models import Chunk, Document, RetrievalOptions
from ai_assistant.core.retrievers import HybridRetriever


def create_chunk(
    content: str,
    source: str,
    chunk_id: int,
) -> Chunk:
    return Chunk(
        content=content,
        document=Document(
            text="",
            source=source,
            title="Test",
        ),
        chunk_id=chunk_id,
    )


def test_hybrid_retriever_combines_results():

    vector_retriever = MagicMock()
    bm25_retriever = MagicMock()

    chunk_1 = create_chunk(
        "semantic result",
        "semantic.txt",
        1,
    )

    chunk_2 = create_chunk(
        "bm25 result",
        "bm25.txt",
        2,
    )

    vector_retriever.retrieve.return_value = [chunk_1]
    bm25_retriever.retrieve.return_value = [chunk_2]

    retriever = HybridRetriever(
        vector_retriever=vector_retriever,
        bm25_retriever=bm25_retriever,
    )

    results = retriever.retrieve(
        "test query",
        RetrievalOptions(
            top_k=2,
            candidate_k=2,
        ),
    )

    assert len(results) == 2

    assert chunk_1 in results
    assert chunk_2 in results


def test_hybrid_retriever_removes_duplicates():

    vector_retriever = MagicMock()
    bm25_retriever = MagicMock()

    chunk = create_chunk(
        "same chunk",
        "document.txt",
        0,
    )

    vector_retriever.retrieve.return_value = [chunk]
    bm25_retriever.retrieve.return_value = [chunk]

    retriever = HybridRetriever(
        vector_retriever=vector_retriever,
        bm25_retriever=bm25_retriever,
    )

    results = retriever.retrieve(
        "test query",
        RetrievalOptions(
            top_k=5,
            candidate_k=5,
        ),
    )

    assert len(results) == 1
    assert results[0] == chunk


def test_hybrid_retriever_uses_rrf_ranking():

    vector_retriever = MagicMock()
    bm25_retriever = MagicMock()

    chunk_a = create_chunk(
        "chunk a",
        "document.txt",
        0,
    )

    chunk_b = create_chunk(
        "chunk b",
        "document.txt",
        1,
    )

    vector_retriever.retrieve.return_value = [
        chunk_a,
        chunk_b,
    ]

    bm25_retriever.retrieve.return_value = [
        chunk_b,
        chunk_a,
    ]

    retriever = HybridRetriever(
        vector_retriever=vector_retriever,
        bm25_retriever=bm25_retriever,
    )

    results = retriever.retrieve(
        "test query",
        RetrievalOptions(
            top_k=2,
            candidate_k=2,
        ),
    )

    assert len(results) == 2

    assert chunk_a in results
    assert chunk_b in results


def test_hybrid_retriever_returns_top_k():

    vector_retriever = MagicMock()
    bm25_retriever = MagicMock()

    chunks = [
        create_chunk(
            f"chunk {i}",
            "document.txt",
            i,
        )
        for i in range(5)
    ]

    vector_retriever.retrieve.return_value = chunks
    bm25_retriever.retrieve.return_value = chunks

    retriever = HybridRetriever(
        vector_retriever=vector_retriever,
        bm25_retriever=bm25_retriever,
    )

    results = retriever.retrieve(
        "test query",
        RetrievalOptions(
            top_k=2,
            candidate_k=5,
        ),
    )

    assert len(results) == 2