from .tool_call_validator import ToolCallValidator
from .tool_registry import ToolRegistry
from ..models import ToolCall, ToolResult


class ToolExecutor:

    def __init__(
        self,
        registry: ToolRegistry,
        validator: ToolCallValidator,
    ) -> None:
        self._registry = registry
        self._validator = validator

    def execute(
        self,
        tool_call: ToolCall,
    ) -> ToolResult:

        self._validator.validate(
            tool_call,
        )

        tool = self._registry.get(
            tool_call.tool_name,
        )

        output = tool.execute(
            tool_call.arguments,
        )

        return ToolResult(
            tool_name=tool_call.tool_name,
            output=output,
            call_id=tool_call.call_id,
        )