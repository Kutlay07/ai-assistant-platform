from typing import Any

from .base_tool import BaseTool


class ToolSchema:

    @staticmethod
    def from_tool(
        tool: BaseTool,
    ) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": dict(
                    tool.parameters,
                ),
            },
        }