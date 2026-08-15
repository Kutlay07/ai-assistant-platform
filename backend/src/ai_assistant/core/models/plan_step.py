from dataclasses import dataclass, field
from typing import Any

from .step_type import StepType


@dataclass(frozen=True)
class PlanStep:
    step_type: StepType
    description: str
    metadata: dict[str, Any] = field(
        default_factory=dict,
    )