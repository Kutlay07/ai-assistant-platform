from ai_assistant.core.assistant import Assistant
from ai_assistant.core.llms import MockLLM
from ai_assistant.core.memory import MockMemory
from ai_assistant.core.models import ToolCall
from ai_assistant.core.prompts import PromptBuilder
from ai_assistant.core.tools import MockTool, ToolRegistry
from ai_assistant.core.workflows import ChatWorkflow


def test_assistant_executes_registered_tool():
    registry = ToolRegistry()
    registry.register(MockTool())

    workflow = ChatWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
    )
    assistant = Assistant(workflow, tool_registry=registry)

    result = assistant.execute_tool(
        ToolCall(
            tool_name="mock",
            arguments={"query": "hello"},
        )
    )

    assert result == "Mock tool response: hello"