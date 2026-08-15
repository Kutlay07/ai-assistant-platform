from dataclasses import dataclass, field

from ..models import Request, StepResult, StepType


@dataclass
class ExecutionContext:
    request: Request
    results: list[StepResult] = field(
        default_factory=list,
    )

    def add_result(
        self,
        result: StepResult,
    ) -> None:
        self.results.append(result)

    def get_last_result(self) -> StepResult | None:
        if not self.results:
            return None

        return self.results[-1]

    def get_final_result(self) -> StepResult | None:
        return self.get_last_result()

    def is_completed(self) -> bool:
        last_result = self.get_last_result()

        if last_result is None:
            return False

        return (
            last_result.step.step_type
            == StepType.FINAL_RESPONSE
        )