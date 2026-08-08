from ai_assistant.core.assistant import Assistant

from ai_assistant.core.embedders import SentenceTransformerEmbedder
from ai_assistant.core.llms import create_llm
from ai_assistant.core.models import Chunk
from ai_assistant.core.prompts import PromptBuilder
from ai_assistant.core.retrievers import Retriever
from ai_assistant.core.services import SearchService
from ai_assistant.core.vector_stores import PostgreSQLVectorStore
from ai_assistant.core.workflows import ChatWorkflow, RAGWorkflow
from ai_assistant.core.tools import ToolRegistry, MockTool
from ai_assistant.core.memory import FileMemory
from ai_assistant.core.config import settings


def create_memory() -> FileMemory:
    return FileMemory(
        settings.memory_path,
    )


def get_memory() -> FileMemory:
    return create_memory()


def create_search_service() -> SearchService:
    embedder = SentenceTransformerEmbedder()

    vector_store = PostgreSQLVectorStore(
        settings.postgres_connection_string,
    )

    retriever = Retriever(
        embedder=embedder,
        vector_store=vector_store,
    )

    return SearchService(
        retriever=retriever,
    )


def create_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    
    registry.register(MockTool())
    
    return registry


def get_assistant() -> Assistant:
    workflow = ChatWorkflow(
        llm=create_llm(),
        prompt_builder=PromptBuilder(),
        memory=create_memory(),
    )

    return Assistant(
        workflow,
        tool_registry=create_tool_registry(),
        )


def get_rag_assistant() -> Assistant:
    workflow = RAGWorkflow(
        llm=create_llm(),
        prompt_builder=PromptBuilder(),
        search_service=create_search_service(),
        memory=create_memory(),
    )

    return Assistant(
        workflow,
        tool_registry=create_tool_registry(),
        )