from dataclasses import dataclass
from typing import TYPE_CHECKING

from .llm_message_role import LLMMessageRole

if TYPE_CHECKING:
    from .tool_call import ToolCall
    from .tool_result import ToolResult


@dataclass(frozen=True)
class LLMMessage:
    role: LLMMessageRole
    content: str | None = None
    tool_call: "ToolCall | None" = None
    tool_result: "ToolResult | None" = None