import pytest

from ai_assistant.core.models import Request, Response
from ai_assistant.core.workflows import AgentWorkflow
from ai_assistant.core.llms import MockLLM, BaseLLM
from ai_assistant.core.prompts import PromptBuilder
from ai_assistant.core.memory import MockMemory
from ai_assistant.core.tools import (
    MockTool,
    ToolRegistry,
    ToolCallValidator,
    )
from ai_assistant.core.planners import MockPlanner
from ai_assistant.core.models import ToolCall
from ai_assistant.core.parsers import ToolCallParser


class MockExecuteTool:

    def __init__(self):
        self.called_with = None

    def __call__(
        self,
        tool_call: ToolCall,
    ) -> str:
        self.called_with = tool_call
        return "tool result"

def test_agent_workflow_returns_response():
    registry = ToolRegistry()
    registry.register(MockTool())
    execute_tool = MockExecuteTool()

    workflow = AgentWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
        planner=MockPlanner(),
        tool_call_parser=ToolCallParser(),
        execute_tool=execute_tool,
    )

    response = workflow.run(Request(input="Hello"))

    assert isinstance(response, Response)


def test_agent_workflow_uses_tool():
    registry = ToolRegistry()
    registry.register(MockTool())
    
    execute_tool = MockExecuteTool()

    workflow = AgentWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
        planner=MockPlanner(),
        tool_call_parser=ToolCallParser(),
        execute_tool=execute_tool,
    )

    response = workflow.run(Request(input="Hello"))

    assert response.output == "tool result"


def test_agent_workflow_stores_messages():
    memory = MockMemory()

    registry = ToolRegistry()
    registry.register(MockTool())

    execute_tool = MockExecuteTool()

    workflow = AgentWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=memory,
        planner=MockPlanner(),
        tool_call_parser=ToolCallParser(),
        execute_tool=execute_tool,
    )

    workflow.run(Request(input="Hello"))

    history = memory.get_history()

    assert {
        "role": "user",
        "content": "Hello",
    } in history

    assert {
        "role": "tool",
        "content": "tool result",
    } in history


def test_agent_workflow_executes_plan_steps():
    memory = MockMemory()

    registry = ToolRegistry()
    registry.register(MockTool())

    execute_tool = MockExecuteTool()

    workflow = AgentWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=memory,
        planner=MockPlanner(),
        tool_call_parser=ToolCallParser(),
        execute_tool=execute_tool,
    )

    workflow.run(Request(input="Hello"))

    history = memory.get_history()

    tool_messages = [
        message
        for message in history
        if message["content"] == "tool result"
    ]
    
    plan = MockPlanner().create_plan(
        Request(input="Hello")
    )

    assert len(tool_messages) == len(plan.steps)


def test_agent_workflow_requires_positive_iterations():
    registry = ToolRegistry()
    registry.register(MockTool())
    
    execute_tool = MockExecuteTool()

    with pytest.raises(ValueError):
        AgentWorkflow(
            llm=MockLLM(),
            prompt_builder=PromptBuilder(),
            memory=MockMemory(),
            planner = MockPlanner(),
            tool_call_parser=ToolCallParser(),
            max_iterations=0,
            execute_tool=execute_tool,
        )


class FakeLLM(BaseLLM):

    def __init__(self, response: str):
        self.response = response

    def generate(self, prompt: str) -> str:
        return self.response

    def generate_with_tools(
        self,
        messages,
        tools,
    ):
        raise NotImplementedError

    def stream(self, prompt: str):
        yield self.response


def test_agent_workflow_executes_tool():

    execute_tool = MockExecuteTool()

    workflow = AgentWorkflow(
        llm=FakeLLM(response="mock:test query"),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
        planner=MockPlanner(),
        tool_call_parser=ToolCallParser(),
        execute_tool=execute_tool,
    )

    response = workflow.run(
        Request(input="test")
    )

    assert response.output == "tool result"

    assert execute_tool.called_with.tool_name == "mock"


def test_agent_workflow_requires_tool_executor():

    execute_tool = MockExecuteTool()

    workflow = AgentWorkflow(
        llm=MockLLM(),
        prompt_builder=PromptBuilder(),
        memory=MockMemory(),
        planner=MockPlanner(),
        tool_call_parser=ToolCallParser(),
    )

    with pytest.raises(RuntimeError):
        workflow.run(
            Request(input="test")
        )