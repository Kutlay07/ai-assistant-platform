"""
Integration tests for real LLM providers.

These tests require valid API credentials and internet access.
"""

import json

import pytest

from ai_assistant.core.config import settings
from ai_assistant.core.llms import GroqProvider
from ai_assistant.core.models import (
    LLMMessage,
    LLMMessageRole,
    ToolCall,
)


pytestmark = pytest.mark.skipif(
    not settings.llm_api_key,
    reason="LLM_API_KEY is not configured.",
)


def test_generate_returns_string():

    llm = GroqProvider()

    response = llm.generate(
        "Say hello in one word.",
    )

    assert isinstance(
        response,
        str,
    )

    assert len(response) > 0


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


def test_groq_provider_returns_tool_call(
    monkeypatch,
):
    provider = GroqProvider()

    response = FakeResponse(
        FakeMessage(
            tool_calls=[
                FakeToolCall(
                    call_id="call_123",
                    name="mock",
                    arguments=json.dumps(
                        {
                            "query": "Hello",
                        },
                    ),
                ),
            ],
        ),
    )

    def fake_create(**kwargs):
        assert kwargs["model"] == provider._model

        assert kwargs["tools"] == [
            {
                "type": "function",
                "function": {
                    "name": "mock",
                },
            },
        ]

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
                content="Use the mock tool.",
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


def test_groq_provider_returns_text_when_no_tool_call(
    monkeypatch,
):
    provider = GroqProvider()

    response = FakeResponse(
        FakeMessage(
            content="Hello!",
        ),
    )

    def fake_create(**kwargs):
        assert kwargs["model"] == provider._model
        assert kwargs["tools"] == []

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