import pytest

from ai_assistant.core.models import ToolCall
from ai_assistant.core.tools import ToolCallValidator


def test_valid_tool_call_passes():

    validator = ToolCallValidator()

    tool_call = ToolCall(
        tool_name="mock",
        arguments={
            "query": "Hello",
        },
        call_id="call_123",
    )

    validator.validate(tool_call)


def test_tool_call_requires_name():

    validator = ToolCallValidator()

    tool_call = ToolCall(
        tool_name="",
        arguments={
            "query": "Hello",
        },
        call_id="call_123",
    )

    with pytest.raises(ValueError):
        validator.validate(tool_call)


def test_tool_call_requires_arguments():

    validator = ToolCallValidator()

    tool_call = ToolCall(
        tool_name="mock",
        arguments={},
        call_id="call_123",
    )

    with pytest.raises(ValueError):
        validator.validate(tool_call)


def test_tool_call_requires_call_id():

    validator = ToolCallValidator()

    tool_call = ToolCall(
        tool_name="mock",
        arguments={
            "query": "Hello",
        },
        call_id="",
    )

    with pytest.raises(
        ValueError,
        match="Tool call ID cannot be empty.",
    ):
        validator.validate(tool_call)