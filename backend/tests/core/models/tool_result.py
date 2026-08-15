from ai_assistant.core.models import ToolResult


def test_tool_result_stores_tool_name_and_output():
    result = ToolResult(
        tool_name="mock",
        output="Mock tool response",
    )

    assert result.tool_name == "mock"
    assert result.output == "Mock tool response"