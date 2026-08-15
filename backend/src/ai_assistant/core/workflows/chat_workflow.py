from collections.abc import Iterator, Sequence
from typing import Any

from ..llms import BaseLLM
from ..memory import BaseMemory
from ..models import (
    LLMMessage,
    LLMMessageRole,
    Request,
    Response,
    ToolCall,
    ToolResult,
)
from ..prompts import PromptBuilder
from ..tools import ToolExecutor
from .base_workflow import BaseWorkflow


class ChatWorkflow(BaseWorkflow):

    def __init__(
        self,
        llm: BaseLLM,
        prompt_builder: PromptBuilder,
        memory: BaseMemory,
        tool_executor: ToolExecutor | None = None,
        tool_schemas: Sequence[dict[str, Any]] | None = None,
        max_tool_calls: int = 10,
    ) -> None:

        if max_tool_calls < 1:
            raise ValueError(
                "max_tool_calls must be greater than 0."
            )

        self._llm = llm
        self._prompt_builder = prompt_builder
        self._memory = memory
        self._tool_executor = tool_executor
        self._tool_schemas = list(tool_schemas or [])
        self._max_tool_calls = max_tool_calls
        
    def _build_prompt(
        self,
        request: Request,
        ) -> str:
        history = self._memory.get_history()

        return self._prompt_builder.build(
            request=request,
            history=history,
        )
        
    def _build_messages(
        self,
        request: Request,
    ) -> list[LLMMessage]:

        prompt = self._build_prompt(request)

        return [
            LLMMessage(
                role=LLMMessageRole.USER,
                content=prompt,
            ),
        ]
        
        
    def _save_conversation(
        self, 
        request: Request, 
        response: str,) -> None:
        
        self._memory.add_message(
            "user",
            request.input,
        )

        self._memory.add_message(
            "assistant",
            response,
        )
        
        
    def stream(
        self, 
        request: Request, 
        ) -> Iterator[str]:
        
        prompt = self._build_prompt(request)
        
        chunks = []
        
        for chunk in self._llm.stream(prompt):
            chunks.append(chunk)
            yield chunk
            
        response = "".join(chunks)
        
        self._save_conversation(request, response)
        
        


    def _run_with_tools(
    self,
    messages: list[LLMMessage],
    ) -> str:

        if self._tool_executor is None:
            result = self._llm.generate_with_tools(
                messages=messages,
                tools=[],
            )

            if isinstance(result, ToolCall):
                raise ValueError(
                    "LLM returned a tool call but no tool executor is configured."
                )

            return result

        for _ in range(self._max_tool_calls):

            result = self._llm.generate_with_tools(
                messages=messages,
                tools=self._tool_schemas,
            )

            if isinstance(result, str):
                return result

            messages.append(
                LLMMessage(
                    role=LLMMessageRole.ASSISTANT,
                    tool_call=result,
                ),
            )

            tool_result = self._tool_executor.execute(
                result,
                )

            messages.append(
                LLMMessage(
                    role=LLMMessageRole.TOOL,
                    tool_result=tool_result,
                ),
            )

        raise RuntimeError(
            "Maximum tool calls exceeded."
        )


    def run(
        self,
        request: Request,
        ) -> Response:

        messages = self._build_messages(request)

        output = self._run_with_tools(messages)

        self._save_conversation(
            request,
            output,
        )

        return Response(
            output=output,
        )