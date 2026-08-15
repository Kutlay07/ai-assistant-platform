import pytest

from ai_assistant.core.models import (
    LLMMessage,
    LLMMessageRole,
    Request,
    Response,
    ToolCall,
)
from ai_assistant.core.tools import (
    MockTool,
    ToolCallValidator,
    ToolExecutor,
    ToolRegistry,
)
from ai_assistant.core.workflows import ChatWorkflow
from ai_assistant.core.llms import MockLLM
from ai_assistant.core.prompts import PromptBuilder
from ai_assistant.core.memory import MockMemory


def test_chat_workflow_returns_response():
    workflow = ChatWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
    )

    response = workflow.run(Request(input="Hello"))

    assert isinstance(response, Response)


def test_chat_workflow_uses_llm():
    workflow = ChatWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
    )

    response = workflow.run(Request(input="Hello"))

    assert response.output.startswith("Mock response:")
    assert "Hello" in response.output


def test_chat_workflow_preserves_request_input():
    workflow = ChatWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
    )

    response = workflow.run(Request(input="How are you?"))

    assert response.output.startswith("Mock response:")
    assert "How are you?" in response.output


class ToolCallingLLM:

    def __init__(self):
        self.calls = []

    def generate(
        self,
        prompt: str,
    ) -> str:
        return "unused"

    def stream(
        self,
        prompt: str,
    ):
        yield "unused"

    def generate_with_tools(
        self,
        messages,
        tools,
    ):
        self.calls.append(
            {
                "messages": messages,
                "tools": tools,
            }
        )

        if len(self.calls) == 1:
            return ToolCall(
                tool_name="mock",
                arguments={
                    "query": "Hello",
                },
                call_id="call_123",
            )

        return "Final answer"


def test_chat_workflow_executes_tool_and_returns_final_response():

    llm = ToolCallingLLM()

    registry = ToolRegistry()
    registry.register(
        MockTool(),
    )

    tool_executor = ToolExecutor(
        registry=registry,
        validator=ToolCallValidator(),
    )

    workflow = ChatWorkflow(
        llm=llm,
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
        tool_executor=tool_executor,
        tool_schemas=[
            {
                "type": "function",
                "function": {
                    "name": "mock",
                },
            },
        ],
    )

    response = workflow.run(
        Request(
            input="Hello",
        ),
    )

    assert response.output == "Final answer"

    assert len(llm.calls) == 2


def test_chat_workflow_passes_tool_result_back_to_llm():

    llm = ToolCallingLLM()

    registry = ToolRegistry()
    registry.register(
        MockTool(),
    )

    tool_executor = ToolExecutor(
        registry=registry,
        validator=ToolCallValidator(),
    )

    workflow = ChatWorkflow(
        llm=llm,
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
        tool_executor=tool_executor,
    )

    workflow.run(
        Request(
            input="Hello",
        ),
    )

    second_call_messages = llm.calls[1]["messages"]

    assert len(second_call_messages) == 3

    assert (
        second_call_messages[0].role
        == LLMMessageRole.USER
    )

    assert (
        second_call_messages[1].role
        == LLMMessageRole.ASSISTANT
    )

    assert (
        second_call_messages[1].tool_call.tool_name
        == "mock"
    )

    assert (
        second_call_messages[2].role
        == LLMMessageRole.TOOL
    )

    assert (
        second_call_messages[2].tool_result.output
        == "Mock tool response: Hello"
    )


class ToolCallingLLMWithoutExecutor:

    def generate(
        self,
        prompt: str,
    ) -> str:
        return "unused"

    def stream(
        self,
        prompt: str,
    ):
        yield "unused"

    def generate_with_tools(
        self,
        messages,
        tools,
    ):
        return ToolCall(
            tool_name="mock",
            arguments={
                "query": "Hello",
            },
            call_id="call_123",
        )


def test_chat_workflow_raises_when_tool_call_has_no_executor():

    workflow = ChatWorkflow(
        llm=ToolCallingLLMWithoutExecutor(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
    )

    with pytest.raises(
        ValueError,
        match="no tool executor is configured",
    ):
        workflow.run(
            Request(
                input="Hello",
            ),
        )


class InfiniteToolCallingLLM:

    def generate(
        self,
        prompt: str,
    ) -> str:
        return "unused"

    def stream(
        self,
        prompt: str,
    ):
        yield "unused"

    def generate_with_tools(
        self,
        messages,
        tools,
    ):
        return ToolCall(
            tool_name="mock",
            arguments={
                "query": "Hello",
            },
            call_id="call_123",
        )


def test_chat_workflow_stops_after_max_tool_calls():

    registry = ToolRegistry()
    registry.register(
        MockTool(),
    )

    tool_executor = ToolExecutor(
        registry=registry,
        validator=ToolCallValidator(),
    )

    workflow = ChatWorkflow(
        llm=InfiniteToolCallingLLM(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
        tool_executor=tool_executor,
        max_tool_calls=2,
    )

    with pytest.raises(
        RuntimeError,
        match="Maximum tool calls exceeded",
    ):
        workflow.run(
            Request(
                input="Hello",
            ),
        )