from abc import ABC, abstractmethod
from typing import Any

from ai_assistant.core.models import PlanStep

from ..execution_context import ExecutionContext


class BaseStepHandler(ABC):

    @abstractmethod
    def can_handle(
        self,
        step: PlanStep,
    ) -> bool:
        pass

    @abstractmethod
    def handle(
        self,
        step: PlanStep,
        context: ExecutionContext,
    ) -> Any:
        pass