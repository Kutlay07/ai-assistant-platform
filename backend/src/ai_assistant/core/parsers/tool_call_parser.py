from .base_parser import BaseParser
from ..models import ToolCall


class ToolCallParser(BaseParser):

    def parse(self, text: str) -> ToolCall:

        tool_name, _, query = text.partition(":")

        if not tool_name or not query:
            raise ValueError(
                "Invalid tool call format."
            )

        return ToolCall(
            tool_name=tool_name.strip(),
            arguments={
                "query": query.strip(),
            },
            call_id="parsed_tool_call",
        )