from ..models import ToolCall


class ToolCallValidator:

    def validate(
        self,
        tool_call: ToolCall,
    ) -> None:

        if not tool_call.tool_name:
            raise ValueError(
                "Tool name cannot be empty."
            )

        if not tool_call.arguments:
            raise ValueError(
                "Tool arguments cannot be empty."
            )

        if not tool_call.call_id:
            raise ValueError(
                "Tool call ID cannot be empty."
            )