from ai_assistant.core.models import ToolResult


def test_tool_result_stores_values():
    result = ToolResult(
        tool_name="mock",
        output="Mock tool response",
        call_id="call_123",
    )

    assert result.tool_name == "mock"
    assert result.output == "Mock tool response"
    assert result.call_id == "call_123"