from abc import ABC, abstractmethod

from ..models import (
    Plan,
    Request,
    StepResult,
)


class BasePlanner(ABC):

    @abstractmethod
    def create_plan(
        self,
        request: Request,
        previous_results: list[StepResult] | None = None,
    ) -> Plan:
        """Create an execution plan for the given request."""
        pass