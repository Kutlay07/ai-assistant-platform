from ai_assistant.core.llms import GroqProvider
from ai_assistant.core.models import (
    LLMMessage,
    LLMMessageRole,
    ToolCall,
    ToolResult,
)
from unittest.mock import Mock


def create_provider() -> GroqProvider:
    provider = GroqProvider.__new__(GroqProvider)
    provider._model = "dummy-model"
    return provider


def create_provider_with_client() -> GroqProvider:
    provider = create_provider()

    provider._client = Mock()

    return provider


def test_serializes_user_message():

    provider = create_provider()

    message = LLMMessage(
        role=LLMMessageRole.USER,
        content="Hello",
    )

    result = provider._serialize_message(message)

    assert result == {
        "role": "user",
        "content": "Hello",
    }


def test_serializes_assistant_tool_call():

    provider = create_provider()

    message = LLMMessage(
        role=LLMMessageRole.ASSISTANT,
        tool_call=ToolCall(
            tool_name="mock",
            arguments={
                "query": "Hello",
            },
            call_id="call_123",
        ),
    )

    result = provider._serialize_message(message)

    assert result == {
        "role": "assistant",
        "tool_calls": [
            {
                "id": "call_123",
                "type": "function",
                "function": {
                    "name": "mock",
                    "arguments": '{"query": "Hello"}',
                },
            },
        ],
    }


def test_serializes_tool_result():

    provider = create_provider()

    message = LLMMessage(
        role=LLMMessageRole.TOOL,
        tool_result=ToolResult(
            tool_name="mock",
            output="Mock tool response: Hello",
            call_id="call_123",
        ),
    )

    result = provider._serialize_message(message)

    assert result == {
        "role": "tool",
        "content": "Mock tool response: Hello",
        "tool_call_id": "call_123",
    }


class FakeMessage:

    def __init__(
        self,
        content: str | None = None,
        tool_calls=None,
    ) -> None:
        self.content = content
        self.tool_calls = tool_calls


class FakeChoice:

    def __init__(
        self,
        message: FakeMessage,
    ) -> None:
        self.message = message


class FakeResponse:

    def __init__(
        self,
        message: FakeMessage,
    ) -> None:
        self.choices = [
            FakeChoice(message),
        ]


class FakeFunction:

    def __init__(
        self,
        name: str,
        arguments: str,
    ) -> None:
        self.name = name
        self.arguments = arguments


class FakeToolCall:

    def __init__(
        self,
        call_id: str,
        name: str,
        arguments: str,
    ) -> None:
        self.id = call_id
        self.function = FakeFunction(
            name=name,
            arguments=arguments,
        )


def test_generate_with_tools_sends_serialized_messages(
    monkeypatch,
):
    provider = create_provider_with_client()

    captured = {}

    response = FakeResponse(
        FakeMessage(
            content="Hello!",
        ),
    )

    def fake_create(**kwargs):
        captured.update(kwargs)
        return response

    monkeypatch.setattr(
        provider._client.chat.completions,
        "create",
        fake_create,
    )

    result = provider.generate_with_tools(
        messages=[
            LLMMessage(
                role=LLMMessageRole.USER,
                content="Hello",
            ),
        ],
        tools=[],
    )

    assert result == "Hello!"

    assert captured["model"] == "dummy-model"

    assert captured["messages"] == [
        {
            "role": "user",
            "content": "Hello",
        },
    ]

    assert captured["tools"] == []


def test_generate_with_tools_returns_tool_call(
    monkeypatch,
):

    provider = create_provider_with_client()

    provider._model = "dummy-model"

    response = FakeResponse(
        FakeMessage(
            tool_calls=[
                FakeToolCall(
                    call_id="call_123",
                    name="mock",
                    arguments='{"query": "Hello"}',
                ),
            ],
        ),
    )

    def fake_create(**kwargs):
        return response

    monkeypatch.setattr(
        provider._client.chat.completions,
        "create",
        fake_create,
    )

    result = provider.generate_with_tools(
        messages=[
            LLMMessage(
                role=LLMMessageRole.USER,
                content="Use mock tool.",
            ),
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "mock",
                },
            },
        ],
    )

    assert result == ToolCall(
        tool_name="mock",
        arguments={
            "query": "Hello",
        },
        call_id="call_123",
    )