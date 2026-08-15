from ai_assistant.core.models import (
    Plan,
    PlanStep,
    Request,
    StepType,
    StepResult,
)

from .base_planner import BasePlanner


class RuleBasedPlanner(BasePlanner):
    """Creates execution plans using simple rule-based heuristics."""

    SEARCH_KEYWORDS = (
        "search",
        "find",
        "lookup",
        "rag",
    )

    CALCULATION_KEYWORDS = (
        "calculate",
        "math",
        "solve",
    )

    def create_plan(
        self,
        request: Request,
        previous_results: list[StepResult] | None = None,
    ) -> Plan:

        message = request.input.lower()

        steps: list[PlanStep] = []

        if self._requires_search(message):
            steps.append(
                PlanStep(
                    step_type=StepType.RETRIEVE,
                    description="Search relevant information",
                )
            )

        if self._requires_calculation(message):
            steps.append(
                PlanStep(
                    step_type=StepType.TOOL,
                    description="Perform calculation",
                )
            )

        steps.append(
            PlanStep(
                step_type=StepType.LLM,
                description="Generate final response",
                metadata={
                    "prompt": request.input,
                },
            )
        )

        steps.append(
            PlanStep(
                step_type=StepType.FINAL_RESPONSE,
                description="Return final response",
            )
        )

        return Plan(
            steps=steps,
        )

    def _requires_search(
        self,
        message: str,
    ) -> bool:

        return any(
            keyword in message
            for keyword in self.SEARCH_KEYWORDS
        )

    def _requires_calculation(
        self,
        message: str,
    ) -> bool:

        return any(
            keyword in message
            for keyword in self.CALCULATION_KEYWORDS
        )