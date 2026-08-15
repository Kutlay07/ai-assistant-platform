from ai_assistant.core.llms import BaseLLM, MockLLM
from ai_assistant.core.models import (
    LLMMessage,
    LLMMessageRole,
)


def test_mock_llm_generates_response():
    llm = MockLLM()

    response = llm.generate("Hello")

    assert response == "Mock response: Hello"


def test_mock_llm_is_base_llm():
    llm = MockLLM()

    assert isinstance(llm, BaseLLM)


def test_mock_llm_generate_with_tools_returns_response():
    llm = MockLLM()

    result = llm.generate_with_tools(
        messages=[
            LLMMessage(
                role=LLMMessageRole.USER,
                content="Hello",
            ),
        ],
        tools=[],
    )

    assert result == "Mock response: Hello"