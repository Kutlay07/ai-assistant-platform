from .base_memory import BaseMemory
from ..summarizers import BaseSummarizer


class SummarizingMemory(BaseMemory):

    def __init__(
        self,
        memory: BaseMemory,
        summarizer: BaseSummarizer,
        max_messages: int = 10,
    ) -> None:

        if max_messages < 1:
            raise ValueError(
                "max_messages must be greater than 0."
            )

        self._memory = memory
        self._summarizer = summarizer
        self._max_messages = max_messages


    def get_history(
        self,
    ) -> list[dict[str, str]]:

        return self._memory.get_history()


    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:

        self._memory.add_message(
            role,
            content,
        )

        history = self._memory.get_history()

        if len(history) > self._max_messages:

            messages_to_summarize = history[
                :len(history) - self._max_messages
            ]

            previous_summary = self._memory.get_summary()

            summary = self._summarizer.summarize(
                messages=messages_to_summarize,
                previous_summary=previous_summary,
            )

            self._memory.save_summary(summary)

            remaining_messages = history[
                -self._max_messages:
            ]

            self._memory.replace_history(
                remaining_messages,
            )

    def get_summary(
        self,
    ) -> str | None:

        return self._memory.get_summary()


    def save_summary(
        self,
        summary: str,
    ) -> None:

        self._memory.save_summary(
            summary,
        )


    def replace_history(
        self,
        history: list[dict[str, str]],
    ) -> None:
        self._memory.replace_history(
            history,
        )