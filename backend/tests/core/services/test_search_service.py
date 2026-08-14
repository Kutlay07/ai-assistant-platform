from ai_assistant.core.services import SearchService
from ai_assistant.core.retrievers import SemanticRetriever
from ai_assistant.core.embedders import MockEmbedder
from ai_assistant.core.vector_stores import MockVectorStore
from ai_assistant.core.models import Chunk
from ai_assistant.core.models import RetrievalOptions


def test_search_returns_chunks():

    store = MockVectorStore()

    store.add([
        Chunk(content="Python is a programming language.")
    ])

    service = SearchService(
        SemanticRetriever(
            embedder=MockEmbedder(),
            vector_store=store,
        )
    )

    chunks = service.search("Python")

    assert len(chunks) == 1


def test_search_preserves_chunk_content():

    store = MockVectorStore()

    store.add([
        Chunk(content="Python is a programming language.")
    ])

    service = SearchService(
        SemanticRetriever(
            embedder=MockEmbedder(),
            vector_store=store,
        )
    )

    chunk = service.search("Python")[0]

    assert chunk.content == "Python is a programming language."


def test_search_returns_empty_list_when_no_chunks():

    service = SearchService(
        SemanticRetriever(
            embedder=MockEmbedder(),
            vector_store=MockVectorStore(),
        )
    )

    chunks = service.search("Python")

    assert chunks == []


def test_search_respects_top_k():

    store = MockVectorStore()

    store.add([
        Chunk(content="A"),
        Chunk(content="B"),
        Chunk(content="C"),
    ])

    service = SearchService(
        SemanticRetriever(
            embedder=MockEmbedder(),
            vector_store=store,
        )
    )

    chunks = service.search(
        "python",
        options = RetrievalOptions(top_k=2),
    )

    assert len(chunks) == 2
    assert chunks[0].content == "A"
    assert chunks[1].content == "B"