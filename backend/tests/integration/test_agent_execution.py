from ai_assistant.core.execution import PlanExecutor
from ai_assistant.core.execution.handlers import (
    FinalResponseStepHandler,
    LLMStepHandler,
)
from ai_assistant.core.llms import MockLLM
from ai_assistant.core.models import Request
from ai_assistant.core.planners import RuleBasedPlanner


def test_rule_based_plan_executes_end_to_end():
    request = Request(
        input="Hello",
    )

    planner = RuleBasedPlanner()

    plan = planner.create_plan(
        request=request,
    )

    executor = PlanExecutor(
        handlers=[
            LLMStepHandler(
                llm=MockLLM(),
            ),
            FinalResponseStepHandler(),
        ],
    )

    context = executor.execute(
        plan=plan,
        request=request,
    )

    assert len(context.results) == 2

    assert (
        context.results[0].output
        == "Mock response: Hello"
    )

    assert (
        context.results[-1].output
        == "Mock response: Hello"
    )