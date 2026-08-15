import pytest

from ai_assistant.core.memory import (
    MockMemory,
    SummarizingMemory,
)
from ai_assistant.core.summarizers import MockSummarizer


def create_memory(
    max_messages: int = 10,
) -> SummarizingMemory:

    return SummarizingMemory(
        memory=MockMemory(),
        summarizer=MockSummarizer(),
        max_messages=max_messages,
    )


def test_summarizing_memory_stores_messages():

    memory = create_memory()

    memory.add_message(
        "user",
        "Hello",
    )

    assert memory.get_history() == [
        {
            "role": "user",
            "content": "Hello",
        },
    ]


def test_summarizing_memory_preserves_message_order():

    memory = create_memory()

    memory.add_message(
        "user",
        "Hello",
    )

    memory.add_message(
        "assistant",
        "Hi!",
    )

    assert memory.get_history() == [
        {
            "role": "user",
            "content": "Hello",
        },
        {
            "role": "assistant",
            "content": "Hi!",
        },
    ]


def test_summarizing_memory_requires_positive_max_messages():

    with pytest.raises(ValueError):
        SummarizingMemory(
            memory=MockMemory(),
            summarizer=MockSummarizer(),
            max_messages=0,
        )


class MockSummarizer:

    def __init__(self):
        self.called_with = None

    def summarize(
        self,
        messages: list[dict[str, str]],
        previous_summary: str | None = None,
    ) -> str:
        self.called_with = {
            "messages": messages,
            "previous_summary": previous_summary,
        }

        return "Conversation summary"


def test_summarizing_memory_summarizes_old_messages():

    memory = MockMemory()

    summarizer = MockSummarizer()

    summarizing_memory = SummarizingMemory(
        memory=memory,
        summarizer=summarizer,
        max_messages=2,
    )

    summarizing_memory.add_message(
        "user",
        "Hello",
    )

    summarizing_memory.add_message(
        "assistant",
        "Hi",
    )

    summarizing_memory.add_message(
        "user",
        "How are you?",
    )

    assert summarizer.called_with is not None


def test_summarizing_memory_summarizes_oldest_messages():

    memory = MockMemory()

    summarizer = MockSummarizer()

    summarizing_memory = SummarizingMemory(
        memory=memory,
        summarizer=summarizer,
        max_messages=2,
    )

    summarizing_memory.add_message(
        "user",
        "First",
    )

    summarizing_memory.add_message(
        "assistant",
        "Second",
    )

    summarizing_memory.add_message(
        "user",
        "Third",
    )

    assert summarizer.called_with["messages"] == [
        {
            "role": "user",
            "content": "First",
        }
    ]


def test_summarizing_memory_saves_summary():

    memory = MockMemory()

    summarizer = MockSummarizer()

    summarizing_memory = SummarizingMemory(
        memory=memory,
        summarizer=summarizer,
        max_messages=2,
    )

    summarizing_memory.add_message(
        "user",
        "First",
    )

    summarizing_memory.add_message(
        "assistant",
        "Second",
    )

    summarizing_memory.add_message(
        "user",
        "Third",
    )

    assert memory.get_summary() == (
        "Conversation summary"
    )


def test_summarizing_memory_removes_summarized_messages():

    memory = MockMemory()

    summarizer = MockSummarizer()

    summarizing_memory = SummarizingMemory(
        memory=memory,
        summarizer=summarizer,
        max_messages=2,
    )

    summarizing_memory.add_message(
        "user",
        "First",
    )

    summarizing_memory.add_message(
        "assistant",
        "Second",
    )

    summarizing_memory.add_message(
        "user",
        "Third",
    )

    assert memory.get_history() == [
        {
            "role": "assistant",
            "content": "Second",
        },
        {
            "role": "user",
            "content": "Third",
        },
    ]


def test_summarizing_memory_uses_previous_summary():

    memory = MockMemory()

    memory.save_summary(
        "Previous conversation summary"
    )

    summarizer = MockSummarizer()

    summarizing_memory = SummarizingMemory(
        memory=memory,
        summarizer=summarizer,
        max_messages=2,
    )

    summarizing_memory.add_message(
        "user",
        "First",
    )

    summarizing_memory.add_message(
        "assistant",
        "Second",
    )

    summarizing_memory.add_message(
        "user",
        "Third",
    )

    assert summarizer.called_with["messages"] == [
        {
            "role": "user",
            "content": "First",
        }
    ]