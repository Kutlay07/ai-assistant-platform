from collections.abc import Iterator, Sequence
from typing import Any

from ai_assistant.core.llms import BaseLLM
from ai_assistant.core.models import (
    LLMMessage,
    ToolCall,
)
from ai_assistant.core.summarizers import (
    BaseSummarizer,
    LLMSummarizer,
)


class FakeLLM(BaseLLM):

    def __init__(self):
        self.prompt = None

    def generate(
        self,
        prompt: str,
    ) -> str:
        self.prompt = prompt

        return "Generated summary"

    def generate_with_tools(
        self,
        messages: Sequence[LLMMessage],
        tools: Sequence[dict[str, Any]],
    ) -> str | ToolCall:
        raise NotImplementedError

    def stream(
        self,
        prompt: str,
    ) -> Iterator[str]:
        raise NotImplementedError


def test_llm_summarizer_sends_messages_to_llm():

    llm = FakeLLM()

    summarizer = LLMSummarizer(
        llm=llm,
    )

    result = summarizer.summarize(
        messages=[
            {
                "role": "user",
                "content": "Hello",
            },
            {
                "role": "assistant",
                "content": "Hi!",
            },
        ],
    )

    assert result == "Generated summary"

    assert "user: Hello" in llm.prompt
    assert "assistant: Hi!" in llm.prompt


def test_llm_summarizer_uses_previous_summary():

    llm = FakeLLM()

    summarizer = LLMSummarizer(
        llm=llm,
    )

    result = summarizer.summarize(
        messages=[
            {
                "role": "user",
                "content": "I like Python",
            },
        ],
        previous_summary="User is learning AI engineering.",
    )

    assert result == "Generated summary"

    assert (
        "User is learning AI engineering."
        in llm.prompt
    )

    assert "user: I like Python" in llm.prompt