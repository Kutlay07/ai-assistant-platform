from ai_assistant.core.models import (
    Plan,
    Request,
    StepType,
)
from ai_assistant.core.planners import MockPlanner


def test_mock_planner_returns_plan():
    planner = MockPlanner()

    plan = planner.create_plan(
        Request(input="Hello")
    )

    assert isinstance(plan, Plan)


def test_mock_planner_contains_single_step():
    planner = MockPlanner()

    plan = planner.create_plan(
        Request(input="Hello")
    )

    assert len(plan.steps) == 1


def test_mock_planner_uses_request_input():
    planner = MockPlanner()

    plan = planner.create_plan(
        Request(input="Hello")
    )

    step = plan.steps[0]

    assert step.step_type == StepType.FINAL_RESPONSE
    assert step.description == "Process request: Hello"