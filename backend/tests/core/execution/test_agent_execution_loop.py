import pytest

from ai_assistant.core.execution import (
    AgentExecutionLoop,
    PlanExecutor,
)
from ai_assistant.core.models import (
    Plan,
    PlanStep,
    Request,
    StepType,
    StepResult,
)
from ai_assistant.core.planners import BasePlanner
from ai_assistant.core.execution.handlers import (
    FinalResponseStepHandler,
    LLMStepHandler,
)
from ai_assistant.core.llms import MockLLM
from ai_assistant.core.execution.exceptions import (
    MaxIterationsExceededError,
)



class FakePlanner(BasePlanner):

    def create_plan(
        self,
        request: Request,
        previous_results: list[StepResult] | None = None,
    ) -> Plan:
        return Plan(
            steps=[
                PlanStep(
                    step_type=StepType.FINAL_RESPONSE,
                    description="Return final response",
                ),
            ],
        )


def test_agent_execution_loop_returns_completed_context():
    planner = FakePlanner()

    executor = PlanExecutor(
        handlers=[
            FinalResponseStepHandler(),
        ],
    )

    loop = AgentExecutionLoop(
        planner=planner,
        executor=executor,
    )

    context = loop.execute(
        Request(
            input="Hello",
        )
    )

    assert context.is_completed()


class IncompletePlanner(BasePlanner):

    def create_plan(
        self,
        request: Request,
        previous_results: list[StepResult] | None = None,
    ) -> Plan:
        return Plan(
            steps=[
                PlanStep(
                    step_type=StepType.LLM,
                    description="Continue reasoning",
                    metadata={
                        "prompt": request.input,
                    },
                ),
            ],
        )


def test_agent_execution_loop_stops_at_max_iterations():
    planner = IncompletePlanner()

    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                MockLLM(),
            ),
        ],
    )

    loop = AgentExecutionLoop(
        planner=planner,
        executor=executor,
        max_iterations=3,
    )

    with pytest.raises(
        MaxIterationsExceededError,
        match="Agent execution exceeded maximum iterations.",
    ):
        loop.execute(
            Request(
                input="Hello",
            )
        )


def test_agent_execution_loop_requires_positive_max_iterations():
    with pytest.raises(
        ValueError,
        match="max_iterations must be greater than 0.",
    ):
        AgentExecutionLoop(
            planner=FakePlanner(),
            executor=PlanExecutor(
                handlers=[
                    FinalResponseStepHandler(),
                ],
            ),
            max_iterations=0,
        )


class MultiIterationPlanner(BasePlanner):

    def __init__(self) -> None:
        self._call_count = 0

    def create_plan(
        self,
        request: Request,
        previous_results: list[StepResult] | None = None,
    ) -> Plan:

        self._call_count += 1

        if self._call_count == 1:
            return Plan(
                steps=[
                    PlanStep(
                        step_type=StepType.LLM,
                        description="First step",
                        metadata={
                            "prompt": "First iteration",
                        },
                    ),
                ],
            )

        return Plan(
            steps=[
                PlanStep(
                    step_type=StepType.FINAL_RESPONSE,
                    description="Return final response",
                ),
            ],
        )


def test_agent_execution_loop_preserves_context_between_iterations():
    planner = MultiIterationPlanner()

    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                MockLLM(),
            ),
            FinalResponseStepHandler(),
        ],
    )

    loop = AgentExecutionLoop(
        planner=planner,
        executor=executor,
        max_iterations=2,
    )

    context = loop.execute(
        Request(
            input="Hello",
        )
    )

    assert len(context.results) == 2

    assert (
        context.results[0].step.step_type
        == StepType.LLM
    )

    assert (
        context.results[1].step.step_type
        == StepType.FINAL_RESPONSE
    )

    assert context.is_completed()


class ContextAwarePlanner(BasePlanner):

    def __init__(self) -> None:
        self.received_results: list[StepResult] | None = None
        self._call_count = 0

    def create_plan(
        self,
        request: Request,
        previous_results: list[StepResult] | None = None,
    ) -> Plan:

        self._call_count += 1

        if self._call_count == 2:
            self.received_results = list(
                previous_results or [],
            )

        if self._call_count == 1:
            return Plan(
                steps=[
                    PlanStep(
                        step_type=StepType.LLM,
                        description="Generate intermediate result",
                        metadata={
                            "prompt": "First step",
                        },
                    ),
                ],
            )

        return Plan(
            steps=[
                PlanStep(
                    step_type=StepType.FINAL_RESPONSE,
                    description="Return final response",
                ),
            ],
        )


def test_agent_execution_loop_passes_previous_results_to_planner():
    planner = ContextAwarePlanner()

    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                MockLLM(),
            ),
            FinalResponseStepHandler(),
        ],
    )

    loop = AgentExecutionLoop(
        planner=planner,
        executor=executor,
        max_iterations=2,
    )

    loop.execute(
        Request(
            input="Hello",
        )
    )

    assert planner.received_results is not None
    assert len(planner.received_results) == 1
    assert (
        planner.received_results[0].step.step_type
        == StepType.LLM
    )


class ResultDrivenPlanner(BasePlanner):

    def create_plan(
        self,
        request: Request,
        previous_results: list[StepResult] | None = None,
    ) -> Plan:

        if not previous_results:
            return Plan(
                steps=[
                    PlanStep(
                        step_type=StepType.LLM,
                        description="Generate intermediate result",
                        metadata={
                            "prompt": request.input,
                        },
                    ),
                ],
            )

        return Plan(
            steps=[
                PlanStep(
                    step_type=StepType.FINAL_RESPONSE,
                    description="Return final response",
                ),
            ],
        )


def test_agent_execution_loop_replans_using_previous_results():
    planner = ResultDrivenPlanner()

    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                MockLLM(),
            ),
            FinalResponseStepHandler(),
        ],
    )

    loop = AgentExecutionLoop(
        planner=planner,
        executor=executor,
        max_iterations=2,
    )

    context = loop.execute(
        Request(
            input="Hello",
        )
    )

    assert len(context.results) == 2

    assert (
        context.results[0].step.step_type
        == StepType.LLM
    )

    assert (
        context.results[1].step.step_type
        == StepType.FINAL_RESPONSE
    )

    assert context.is_completed()