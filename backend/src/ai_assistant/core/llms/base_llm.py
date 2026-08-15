from abc import ABC, abstractmethod
from collections.abc import Iterator, Sequence
from typing import Any

from ..models import (
    ToolCall,
    LLMMessage,
)


class BaseLLM(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """Generate a response from the given prompt."""
        pass

    @abstractmethod
    def generate_with_tools(
        self,
        messages: Sequence[LLMMessage],
        tools: Sequence[dict[str, Any]],
    ) -> str | ToolCall:
        """Generate a response or select a tool to call."""
        pass

    @abstractmethod
    def stream(
        self,
        prompt: str,
    ) -> Iterator[str]:
        """Stream a response from the given prompt."""
        pass