from typing import Any

from ai_assistant.core.models import (
    Plan,
    PlanStep,
    Request,
    StepResult,
    StepType,
)

from .exceptions import StepExecutionError
from .execution_context import ExecutionContext
from .handlers.base_step_handler import BaseStepHandler


class PlanExecutor:

    def __init__(
        self,
        handlers: list[BaseStepHandler],
    ) -> None:
        self._handlers = handlers

    def execute(
        self,
        plan: Plan,
        request: Request,
        context: ExecutionContext | None = None,
    ) -> ExecutionContext:

        if context is None:
            context = ExecutionContext(
                request=request,
            )

        for step in plan.steps:
            result = self._execute_step(
                step=step,
                context=context,
            )

            context.add_result(
                StepResult(
                    step=step,
                    output=result,
                )
            )

            if context.is_completed():
                break

        return context

    def _execute_step(
        self,
        step: PlanStep,
        context: ExecutionContext,
    ) -> Any:

        for handler in self._handlers:
            if handler.can_handle(step):
                return handler.handle(
                    step=step,
                    context=context,
                )

        raise StepExecutionError(
            f"No handler found for step: {step}"
        )