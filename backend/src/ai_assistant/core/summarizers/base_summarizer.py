from abc import ABC, abstractmethod
from collections.abc import Sequence


class BaseSummarizer(ABC):

    @abstractmethod
    def summarize(
        self,
        messages: Sequence[dict[str, str]],
        previous_summary: str | None = None,
    ) -> str:
        """Summarize conversation messages."""
        pass