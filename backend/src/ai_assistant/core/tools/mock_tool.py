from collections.abc import Mapping
from typing import Any

from .base_tool import BaseTool


class MockTool(BaseTool):

    @property
    def name(self) -> str:
        return "mock"

    @property
    def description(self) -> str:
        return "A mock tool used for testing."

    @property
    def parameters(self) -> Mapping[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to process.",
                },
            },
            "required": [
                "query",
            ],
        }

    def execute(
        self,
        arguments: Mapping[str, Any],
    ) -> str:
        return f"Mock tool response: {arguments['query']}"