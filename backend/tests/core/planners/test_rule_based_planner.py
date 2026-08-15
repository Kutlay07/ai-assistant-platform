from ai_assistant.core.models import (
    Request,
    StepType,
)
from ai_assistant.core.planners import RuleBasedPlanner


def test_search_request_creates_retrieval_plan():
    planner = RuleBasedPlanner()

    plan = planner.create_plan(
        Request(input="Search FastAPI documentation")
    )

    assert [
        step.step_type
        for step in plan.steps
    ] == [
        StepType.RETRIEVE,
        StepType.LLM,
        StepType.FINAL_RESPONSE,
    ]


def test_calculation_request_creates_tool_plan():
    planner = RuleBasedPlanner()

    plan = planner.create_plan(
        Request(input="Calculate 2 + 2")
    )

    assert [
        step.step_type
        for step in plan.steps
    ] == [
        StepType.TOOL,
        StepType.LLM,
        StepType.FINAL_RESPONSE,
    ]


def test_search_and_calculation_request():
    planner = RuleBasedPlanner()

    plan = planner.create_plan(
        Request(input="Search and calculate")
    )

    assert [
        step.step_type
        for step in plan.steps
    ] == [
        StepType.RETRIEVE,
        StepType.TOOL,
        StepType.LLM,
        StepType.FINAL_RESPONSE,
    ]


def test_regular_chat_creates_response_plan():
    planner = RuleBasedPlanner()

    plan = planner.create_plan(
        Request(input="Hello")
    )

    assert [
        step.step_type
        for step in plan.steps
    ] == [
        StepType.LLM,
        StepType.FINAL_RESPONSE,
    ]


def test_llm_step_uses_request_as_prompt():
    planner = RuleBasedPlanner()

    request = Request(
        input="Hello",
    )

    plan = planner.create_plan(
        request,
    )

    llm_step = plan.steps[-2]

    assert llm_step.metadata["prompt"] == request.input