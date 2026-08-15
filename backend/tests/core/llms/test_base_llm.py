from ai_assistant.core.llms import BaseLLM
from typing import Any
from collections.abc import Sequence

from ai_assistant.core.models import ToolCall


class DummyLLM(BaseLLM):
    def generate(self, prompt: str) -> str:
        return "dummy"
    
    def stream(self, prompt):
        yield self.generate(prompt)
        
    def generate_with_tools(
    self,
    prompt: str,
    tools: Sequence[dict[str, Any]],
    ) -> str | ToolCall:
        
        return self.generate(
            prompt,
        )

def test_base_llm_generate():
    llm = DummyLLM()
    
    response = llm.generate("Hello")
    
    assert response == "dummy"


def test_base_llm_is_instantiable_through_subclass():
    llm = DummyLLM()
    
    assert isinstance(llm, BaseLLM)