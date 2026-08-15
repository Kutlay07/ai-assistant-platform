from dataclasses import dataclass
from collections.abc import Mapping
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    arguments: Mapping[str, Any]
    call_id: str