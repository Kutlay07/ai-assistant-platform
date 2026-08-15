from dataclasses import dataclass
from typing import Any

from .plan_step import PlanStep


@dataclass(frozen=True)
class StepResult:
    step: PlanStep
    output: Any