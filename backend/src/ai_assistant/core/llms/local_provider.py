from collections.abc import Sequence
from typing import Any

from ..models import ToolCall
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
        prompt: str,
        tools: Sequence[dict[str, Any]],
    ) -> str | ToolCall:
        raise NotImplementedError(
            "Local provider is not implemented yet."
        )