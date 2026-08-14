from fastapi import Request

from ai_assistant.core.assistant import Assistant
from ai_assistant.core.llms import create_llm
from ai_assistant.core.memory import FileMemory
from ai_assistant.core.prompts import PromptBuilder
from ai_assistant.core.services import SearchService
from ai_assistant.core.tools import MockTool, ToolRegistry
from ai_assistant.core.workflows import ChatWorkflow, RAGWorkflow


def get_memory(request: Request) -> FileMemory:
    return request.app.state.memory


def get_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(MockTool())
    return registry


def get_search_service(request: Request) -> SearchService:
    try:
        return request.app.state.search_service
    except AttributeError:
        raise RuntimeError("SearchService is not initialized on app.state.")


def get_assistant(request: Request) -> Assistant:
    workflow = ChatWorkflow(
        llm=create_llm(),
        prompt_builder=PromptBuilder(),
        memory=get_memory(request),
    )

    return Assistant(
        workflow,
        tool_registry=get_tool_registry(),
    )


def get_rag_assistant(request: Request) -> Assistant:
    workflow = RAGWorkflow(
        llm=create_llm(),
        prompt_builder=PromptBuilder(),
        search_service=get_search_service(request),
        memory=get_memory(request),
    )

    return Assistant(
        workflow,
        tool_registry=get_tool_registry(),
    )