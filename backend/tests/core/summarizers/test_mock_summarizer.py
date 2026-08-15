from ai_assistant.core.summarizers import MockSummarizer


def test_mock_summarizer_summarizes_messages():

    summarizer = MockSummarizer()

    result = summarizer.summarize(
        [
            {
                "role": "user",
                "content": "Hello",
            },
            {
                "role": "assistant",
                "content": "Hi!",
            },
        ]
    )

    assert result == "Hello | Hi!"


def test_mock_summarizer_handles_empty_messages():

    summarizer = MockSummarizer()

    result = summarizer.summarize([])

    assert result == ""