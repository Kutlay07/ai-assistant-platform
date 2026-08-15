from collections.abc import Sequence

from .base_summarizer import BaseSummarizer


class MockSummarizer(BaseSummarizer):

    def __init__(self):
        self.called_with = None

    def summarize(
        self,
        messages: Sequence[dict[str, str]],
        previous_summary: str | None = None,
    ) -> str:
        self.called_with = {
            "messages": list(messages),
            "previous_summary": previous_summary,
        }

        summary = " | ".join(
            message["content"]
            for message in messages
        )

        if previous_summary:
            return (
                f"{previous_summary} | {summary}"
                if summary
                else previous_summary
            )

        return summary