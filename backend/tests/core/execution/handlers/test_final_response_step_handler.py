from ai_assistant.core.execution import ExecutionContext
from ai_assistant.core.execution.handlers import (
    FinalResponseStepHandler,
)
from ai_assistant.core.models import (
    PlanStep,
    Request,
    StepResult,
    StepType,
)


def test_final_response_handler_handles_final_response_step():
    handler = FinalResponseStepHandler()

    step = PlanStep(
        step_type=StepType.FINAL_RESPONSE,
        description="Return final response",
    )

    assert handler.can_handle(step)


def test_final_response_handler_does_not_handle_other_steps():
    handler = FinalResponseStepHandler()

    step = PlanStep(
        step_type=StepType.LLM,
        description="Generate response",
    )

    assert not handler.can_handle(step)


def test_final_response_handler_returns_last_result():
    handler = FinalResponseStepHandler()

    request = Request(
        input="Hello",
    )

    context = ExecutionContext(
        request=request,
    )

    previous_step = PlanStep(
        step_type=StepType.LLM,
        description="Generate response",
    )

    context.add_result(
        StepResult(
            step=previous_step,
            output="Generated response",
        )
    )

    final_step = PlanStep(
        step_type=StepType.FINAL_RESPONSE,
        description="Return final response",
    )

    result = handler.handle(
        step=final_step,
        context=context,
    )

    assert result == "Generated response"


def test_final_response_handler_returns_request_input_without_results():
    handler = FinalResponseStepHandler()

    request = Request(
        input="Hello",
    )

    context = ExecutionContext(
        request=request,
    )

    step = PlanStep(
        step_type=StepType.FINAL_RESPONSE,
        description="Return final response",
    )

    result = handler.handle(
        step=step,
        context=context,
    )

    assert result == "Hello"