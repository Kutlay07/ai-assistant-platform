import pytest

from ai_assistant.core.execution import (
    PlanExecutor,
    StepExecutionError,
)
from ai_assistant.core.execution.handlers import (
    LLMStepHandler,
    FinalResponseStepHandler,
)
from ai_assistant.core.llms import MockLLM
from ai_assistant.core.models import (
    Plan,
    PlanStep,
    Request,
    StepType,
)


def test_plan_executor_executes_llm_steps():
    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                llm=MockLLM(),
            ),
        ],
    )

    plan = Plan(
        steps=[
            PlanStep(
                step_type=StepType.LLM,
                description="First step",
                metadata={
                    "prompt": "First prompt",
                },
            ),
            PlanStep(
                step_type=StepType.LLM,
                description="Second step",
                metadata={
                    "prompt": "Second prompt",
                },
            ),
        ],
    )

    context = executor.execute(
        plan=plan,
        request=Request(
            input="Hello",
        ),
    )

    assert len(context.results) == 2

    assert context.results[0].output == (
        "Mock response: First prompt"
    )

    assert context.results[1].output == (
        "Mock response: Second prompt"
    )


def test_plan_executor_executes_plan_and_returns_final_response():
    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                llm=MockLLM(),
            ),
            FinalResponseStepHandler(),
        ],
    )

    plan = Plan(
        steps=[
            PlanStep(
                step_type=StepType.LLM,
                description="Generate response",
                metadata={
                    "prompt": "Hello",
                },
            ),
            PlanStep(
                step_type=StepType.FINAL_RESPONSE,
                description="Return final response",
            ),
        ],
    )

    context = executor.execute(
        plan=plan,
        request=Request(
            input="Hello",
        ),
    )

    assert len(context.results) == 2

    assert context.results[0].output == (
        "Mock response: Hello"
    )

    assert context.results[1].output == (
        "Mock response: Hello"
    )


def test_plan_executor_stops_after_final_response():
    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                llm=MockLLM(),
            ),
            FinalResponseStepHandler(),
        ],
    )

    plan = Plan(
        steps=[
            PlanStep(
                step_type=StepType.LLM,
                description="Generate first response",
                metadata={
                    "prompt": "First",
                },
            ),
            PlanStep(
                step_type=StepType.FINAL_RESPONSE,
                description="Return final response",
            ),
            PlanStep(
                step_type=StepType.LLM,
                description="This should not execute",
                metadata={
                    "prompt": "Second",
                },
            ),
        ],
    )

    context = executor.execute(
        plan=plan,
        request=Request(
            input="Hello",
        ),
    )

    assert len(context.results) == 2

    assert context.results[0].output == (
        "Mock response: First"
    )

    assert context.results[1].output == (
        "Mock response: First"
    )


def test_plan_executor_raises_error_when_no_handler_exists():
    executor = PlanExecutor(
        handlers=[],
    )

    plan = Plan(
        steps=[
            PlanStep(
                step_type=StepType.LLM,
                description="Generate response",
                metadata={
                    "prompt": "Hello",
                },
            ),
        ],
    )

    with pytest.raises(StepExecutionError):
        executor.execute(
            plan=plan,
            request=Request(
                input="Hello",
            ),
        )


def test_plan_executor_propagates_step_execution_error():
    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                llm=MockLLM(),
            ),
        ],
    )

    plan = Plan(
        steps=[
            PlanStep(
                step_type=StepType.LLM,
                description="Generate response",
                metadata={},
            ),
        ],
    )

    with pytest.raises(
        StepExecutionError,
        match="LLM step requires a string prompt.",
    ):
        executor.execute(
            plan=plan,
            request=Request(
                input="Hello",
            ),
        )



from ai_assistant.core.execution import (
    PlanExecutor,
    StepExecutionError,
)
from ai_assistant.core.execution.execution_context import (
    ExecutionContext,
)
from ai_assistant.core.execution.handlers import (
    BaseStepHandler,
)
from ai_assistant.core.models import (
    Plan,
    PlanStep,
    Request,
    StepType,
)


class FailingHandler(BaseStepHandler):

    def can_handle(
        self,
        step: PlanStep,
    ) -> bool:
        return True

    def handle(
        self,
        step: PlanStep,
        context: ExecutionContext,
    ) -> str:
        raise RuntimeError("Something failed")


def test_executor_propagates_handler_error():
    executor = PlanExecutor(
        handlers=[
            FailingHandler(),
        ],
    )

    plan = Plan(
        steps=[
            PlanStep(
                step_type=StepType.LLM,
                description="Generate response",
            )
        ]
    )

    with pytest.raises(RuntimeError):
        executor.execute(
            plan=plan,
            request=Request(
                input="Hello",
            ),
        )


def test_executor_stops_after_final_response():
    llm = MockLLM()

    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(llm),
            FinalResponseStepHandler(),
        ],
    )

    plan = Plan(
        steps=[
            PlanStep(
                step_type=StepType.LLM,
                description="Generate response",
                metadata={"prompt": "Hello"},
            ),
            PlanStep(
                step_type=StepType.FINAL_RESPONSE,
                description="Return final response",
            ),
            PlanStep(
                step_type=StepType.LLM,
                description="Must not execute",
                metadata={
                    "prompt": "This must not execute",
                },
            ),
        ],
    )

    context = executor.execute(
        plan=plan,
        request=Request(input="Hello"),
    )

    assert len(context.results) == 2
    assert (
        context.results[-1].step.step_type
        == StepType.FINAL_RESPONSE
    )