from ai_assistant.core.llms import MockLLM
from ai_assistant.core.memory import MockMemory
from ai_assistant.core.models import Request, Response
from ai_assistant.core.prompts import PromptBuilder
from ai_assistant.core.services import SearchService
from ai_assistant.core.retrievers import SemanticRetriever
from ai_assistant.core.embedders import MockEmbedder
from ai_assistant.core.vector_stores import MockVectorStore
from ai_assistant.core.workflows import RAGWorkflow
from ai_assistant.core.models import Chunk


def test_run_returns_response():

    workflow = RAGWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        search_service=SearchService(
            SemanticRetriever(
                embedder=MockEmbedder(),
                vector_store=MockVectorStore(),
            )
        ),
        memory=MockMemory(),
    )

    response = workflow.run(Request(input="Hello"))

    assert isinstance(response, Response)


def test_run_stores_conversation():

    memory = MockMemory()

    workflow = RAGWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        search_service=SearchService(
            SemanticRetriever(
                embedder=MockEmbedder(),
                vector_store=MockVectorStore(),
            )
        ),
        memory=memory,
    )

    workflow.run(Request(input="Hello"))

    history = memory.get_history()

    assert len(history) == 2


def test_run_uses_retrieved_context():

    store = MockVectorStore()

    store.add([
        Chunk(content="Python is a programming language.")
    ])

    workflow = RAGWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        search_service=SearchService(
            SemanticRetriever(
                embedder=MockEmbedder(),
                vector_store=store,
            )
        ),
        memory=MockMemory(),
    )

    response = workflow.run(
        Request(input="What is Python?")
    )

    assert "Python is a programming language." in response.output


def test_run_builds_rag_prompt():

    workflow = RAGWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        search_service=SearchService(
            SemanticRetriever(
                embedder=MockEmbedder(),
                vector_store=MockVectorStore(),
            )
        ),
        memory=MockMemory(),
    )

    response = workflow.run(
        Request(input="Hello")
    )

    assert "Context:" in response.output