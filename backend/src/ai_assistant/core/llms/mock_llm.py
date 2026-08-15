from .base_llm import BaseLLM
from collections.abc import Iterator, Sequence
from typing import Any

from ..models import (
    ToolCall,
    LLMMessage,
)


class MockLLM(BaseLLM):
    
    def generate(self, prompt: str) -> str:
        return f"Mock response: {prompt}"

    
    def stream(self, prompt: str) -> Iterator[str]:
        response = self.generate(prompt)
        
        for word in response.split():
            yield word + " "
    
    def generate_with_tools(
        self,
        messages: Sequence[LLMMessage],
        tools: Sequence[dict[str, Any]],
    ) -> str | ToolCall:
        last_message = messages[-1]

        if last_message.content:
            return self.generate(
                last_message.content,
            )

        return self.generate(
            "",
        )