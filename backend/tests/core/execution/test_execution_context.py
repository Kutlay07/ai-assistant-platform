from ai_assistant.core.execution import ExecutionContext
from ai_assistant.core.models import (
    PlanStep,
    Request,
    StepResult,
    StepType,
)


def test_execution_context_returns_final_result():
    context = ExecutionContext(
        request=Request(
            input="Hello",
        ),
    )

    step = PlanStep(
        step_type=StepType.LLM,
        description="Generate response",
    )

    result = StepResult(
        step=step,
        output="Hello!",
    )

    context.add_result(result)

    assert context.get_final_result() == result


def test_execution_context_returns_none_without_results():
    context = ExecutionContext(
        request=Request(
            input="Hello",
        ),
    )

    assert context.get_final_result() is None