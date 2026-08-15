from ..models import (
    Plan,
    PlanStep,
    Request,
    StepResult,
    StepType,
)

from .base_planner import BasePlanner


class MockPlanner(BasePlanner):

    def create_plan(
        self,
        request: Request,
        previous_results: list[StepResult] | None = None,
    ) -> Plan:
        return Plan(
            steps=[
                PlanStep(
                    step_type=StepType.FINAL_RESPONSE,
                    description=(
                        f"Process request: {request.input}"
                    ),
                ),
            ],
        )