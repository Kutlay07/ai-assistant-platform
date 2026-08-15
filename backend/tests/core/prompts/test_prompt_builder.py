from ai_assistant.core.models import Request
from ai_assistant.core.prompts import PromptBuilder


def test_prompt_builder_returns_string():
    builder = PromptBuilder()

    prompt = builder.build(
        request=Request(input="Hello"),
        history=[],
        current_step="Process request: Hello",
    )

    assert isinstance(prompt, str)


def test_prompt_builder_includes_user_input():
    builder = PromptBuilder()

    prompt = builder.build(
        request=Request(input="Hello"),
        history=[],
        current_step="Process request: Hello",
    )

    assert "Hello" in prompt


def test_prompt_builder_includes_history():
    builder = PromptBuilder()

    prompt = builder.build(
        request=Request(input="Hello"),
        history=[
            {
                "role": "user",
                "content": "Hello",
            },
            {
                "role": "assistant",
                "content": "Hi",
            },
        ],
        current_step="Process request: Hello",
    )

    assert "Hi" in prompt


def test_prompt_contains_current_step():
    builder = PromptBuilder()

    prompt = builder.build(
        request=Request(input="Hello"),
        history=[],
        current_step="Process request: Hello",
    )

    assert "Current Step:" in prompt
    assert "Process request: Hello" in prompt


def test_prompt_builder_includes_summary():

    builder = PromptBuilder()

    prompt = builder.build(
        request=Request(input="What should I learn next?"),
        history=[],
        summary="User is learning AI engineering.",
    )

    assert "User is learning AI engineering." in prompt