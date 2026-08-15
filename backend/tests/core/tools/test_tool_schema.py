from ai_assistant.core.tools import (
    MockTool,
    ToolSchema,
)


def test_tool_schema_creates_openai_compatible_schema():
    tool = MockTool()

    schema = ToolSchema.from_tool(
        tool,
    )

    assert schema == {
        "type": "function",
        "function": {
            "name": "mock",
            "description": (
                "A mock tool used for testing."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "The query to process."
                        ),
                    },
                },
                "required": [
                    "query",
                ],
            },
        },
    }