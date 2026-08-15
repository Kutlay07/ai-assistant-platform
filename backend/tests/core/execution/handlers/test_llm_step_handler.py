import pytest

from ai_assistant.core.execution import ExecutionContext
from ai_assistant.core.execution.exceptions import StepExecutionError
from ai_assistant.core.execution.handlers import LLMStepHandler
from ai_assistant.core.llms import MockLLM
from ai_assistant.core.models import (
    PlanStep,
    Request,
    StepType,
)


def test_llm_step_handler_handles_llm_step():
    handler = LLMStepHandler(
        llm=MockLLM(),
    )

    step = PlanStep(
        step_type=StepType.LLM,
        description="Generate a response",
        metadata={
            "prompt": "Hello",
        },
    )

    assert handler.can_handle(step)


def test_llm_step_handler_does_not_handle_other_steps():
    handler = LLMStepHandler(
        llm=MockLLM(),
    )

    step = PlanStep(
        step_type=StepType.RETRIEVE,
        description="Retrieve information",
    )

    assert not handler.can_handle(step)


def test_llm_step_handler_generates_response():
    handler = LLMStepHandler(
        llm=MockLLM(),
    )

    request = Request(
        input="Hello",
    )

    context = ExecutionContext(
        request=request,
    )

    step = PlanStep(
        step_type=StepType.LLM,
        description="Generate a response",
        metadata={
            "prompt": "Hello",
        },
    )

    result = handler.handle(
        step=step,
        context=context,
    )

    assert result == "Mock response: Hello"


def test_llm_step_handler_requires_string_prompt():
    handler = LLMStepHandler(
        llm=MockLLM(),
    )

    context = ExecutionContext(
        request=Request(
            input="Hello",
        ),
    )

    step = PlanStep(
        step_type=StepType.LLM,
        description="Generate a response",
    )

    with pytest.raises(
        StepExecutionError,
        match="LLM step requires a string prompt.",
    ):
        handler.handle(
            step=step,
            context=context,
        )