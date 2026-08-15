from ai_assistant.core.models import (
    LLMMessage,
    LLMMessageRole,
    ToolCall,
    ToolResult,
)


def test_llm_message_stores_user_message():
    message = LLMMessage(
        role=LLMMessageRole.USER,
        content="Hello",
    )

    assert message.role == LLMMessageRole.USER
    assert message.content == "Hello"
    assert message.tool_call is None
    assert message.tool_result is None


def test_llm_message_stores_tool_call():
    tool_call = ToolCall(
        tool_name="mock",
        arguments={
            "query": "Hello",
        },
        call_id="call_123",
    )

    message = LLMMessage(
        role=LLMMessageRole.ASSISTANT,
        tool_call=tool_call,
    )

    assert message.role == LLMMessageRole.ASSISTANT
    assert message.tool_call == tool_call
    assert message.content is None


def test_llm_message_stores_tool_result():
    tool_result = ToolResult(
        tool_name="mock",
        output="Mock tool response: Hello",
        call_id="call_123"
    )

    message = LLMMessage(
        role=LLMMessageRole.TOOL,
        tool_result=tool_result,
    )

    assert message.role == LLMMessageRole.TOOL
    assert message.tool_result == tool_result
    assert message.content is None