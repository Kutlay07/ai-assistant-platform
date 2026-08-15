from ai_assistant.core.execution.exceptions import (
    StepExecutionError,
)
from ai_assistant.core.execution.execution_context import (
    ExecutionContext,
)
from ai_assistant.core.llms import BaseLLM
from ai_assistant.core.models import (
    PlanStep,
    StepType,
)

from .base_step_handler import BaseStepHandler


class LLMStepHandler(BaseStepHandler):

    def __init__(
        self,
        llm: BaseLLM,
    ) -> None:
        self._llm = llm

    def can_handle(
        self,
        step: PlanStep,
    ) -> bool:
        return step.step_type == StepType.LLM

    def handle(
        self,
        step: PlanStep,
        context: ExecutionContext,
    ) -> str:

        prompt = step.metadata.get(
            "prompt",
        )

        if not isinstance(prompt, str):
            raise StepExecutionError(
                "LLM step requires a string prompt."
            )

        return self._llm.generate(
            prompt=prompt,
        )