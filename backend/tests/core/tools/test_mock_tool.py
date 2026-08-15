from ai_assistant.core.tools import MockTool


def test_mock_tool_returns_response():
    tool = MockTool()

    result = tool.execute(
        {"query": "Hello"},
    )

    assert result == "Mock tool response: Hello"


def test_mock_tool_returns_string():
    tool = MockTool()

    result = tool.execute(
        {"query": "Hello"},
    )

    assert isinstance(result, str)


def test_mock_tool_name():
    tool = MockTool()

    assert tool.name == "mock"


def test_mock_tool_has_description():
    tool = MockTool()

    assert isinstance(
        tool.description,
        str,
    )

    assert tool.description


def test_mock_tool_has_parameters():
    tool = MockTool()

    assert tool.parameters == {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to process.",
            },
        },
        "required": [
            "query",
        ],
    }