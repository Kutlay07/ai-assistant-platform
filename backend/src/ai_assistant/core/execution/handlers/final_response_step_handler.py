from ai_assistant.core.execution.execution_context import (
    ExecutionContext,
)
from ai_assistant.core.models import (
    PlanStep,
    StepType,
)

from .base_step_handler import BaseStepHandler


class FinalResponseStepHandler(BaseStepHandler):

    def can_handle(
        self,
        step: PlanStep,
    ) -> bool:
        return step.step_type == StepType.FINAL_RESPONSE

    def handle(
        self,
        step: PlanStep,
        context: ExecutionContext,
    ) -> str:
        result = context.get_last_result()

        if result is None:
            return context.request.input

        return str(result.output)