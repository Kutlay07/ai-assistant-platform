from collections.abc import Iterator, Sequence
from typing import Any

from ..models import LLMMessage, ToolCall
from .base_llm import BaseLLM


class LocalProvider(BaseLLM):
    """Placeholder for future local LLM integrations."""

    def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError(
            "Local provider is not implemented yet."
        )

    def generate_with_tools(
        self,
        messages: Sequence[LLMMessage],
        tools: Sequence[dict[str, Any]],
    ) -> str | ToolCall:
        raise NotImplementedError(
            "Local provider is not implemented yet."
        )

    def stream(
        self,
        prompt: str,
    ) -> Iterator[str]:
        raise NotImplementedError(
            "Local provider is not implemented yet."
        )