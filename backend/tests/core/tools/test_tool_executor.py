import pytest

from ai_assistant.core.models import ToolCall
from ai_assistant.core.tools import (
    MockTool,
    ToolCallValidator,
    ToolExecutor,
    ToolRegistry,
)


def test_tool_executor_executes_tool_call():
    registry = ToolRegistry()

    registry.register(
        MockTool(),
    )

    executor = ToolExecutor(
        registry=registry,
        validator=ToolCallValidator(),
    )

    result = executor.execute(
        ToolCall(
            tool_name="mock",
            arguments={
                "query": "Hello",
            },
            call_id="call_123",
        )
    )

    assert result.tool_name == "mock"
    assert result.output == (
        "Mock tool response: Hello"
    )


def test_tool_executor_propagates_validation_error():
    registry = ToolRegistry()

    registry.register(
        MockTool(),
    )

    executor = ToolExecutor(
        registry=registry,
        validator=ToolCallValidator(),
    )

    with pytest.raises(
        ValueError,
        match="Tool arguments cannot be empty.",
    ):
        executor.execute(
            ToolCall(
                tool_name="mock",
                arguments={},
                call_id="call_123",
            )
        )