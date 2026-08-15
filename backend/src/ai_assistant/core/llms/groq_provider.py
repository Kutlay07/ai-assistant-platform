from openai import OpenAI
from collections.abc import Iterator, Sequence
from typing import Any
import json

from .base_llm import BaseLLM
from ..config import settings
from ..models import (
    ToolCall,
    LLMMessage,
    LLMMessageRole,
)


class GroqProvider(BaseLLM):
    
    def __init__(self):
        api_key = settings.llm_api_key
        base_url = settings.llm_base_url
        model = settings.llm_model

        if not api_key:
            raise ValueError("LLM_API_KEY is not configured.")

        if not base_url:
            raise ValueError("LLM_BASE_URL is not configured.")

        if not model:
            raise ValueError("LLM_MODEL is not configured.")

        self._model = model

        self._client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        
        
    def generate(self, prompt: str) -> str:
        
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        
        return response.choices[0].message.content


    def generate_with_tools(
        self,
        messages: Sequence[LLMMessage],
        tools: Sequence[dict[str, Any]],
    ) -> str | ToolCall:

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                self._serialize_message(message)
                for message in messages
            ],
            tools=list(tools),
        )

        message = response.choices[0].message

        if message.tool_calls:
            tool_call = message.tool_calls[0]

            arguments = json.loads(
                tool_call.function.arguments,
            )

            return ToolCall(
                tool_name=tool_call.function.name,
                arguments=arguments,
                call_id=tool_call.id,
            )

        return message.content or ""


    def stream(self, prompt: str) -> Iterator[str]:
        stream = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=True,
        )
        
        for chunk in stream:
            content = chunk.choices[0].delta.content
            
            if content:
                yield content
    
    
    def _serialize_message(
    self,
    message: LLMMessage,
    ) -> dict[str, Any]:

        if message.role == LLMMessageRole.USER:
            return {
                "role": "user",
                "content": message.content or "",
            }

        if message.role == LLMMessageRole.ASSISTANT:
            if message.tool_call is not None:
                return {
                    "role": "assistant",
                    "tool_calls": [
                        {
                            "id": message.tool_call.call_id,
                            "type": "function",
                            "function": {
                                "name": message.tool_call.tool_name,
                                "arguments": json.dumps(
                                    dict(
                                        message.tool_call.arguments,
                                    ),
                                ),
                            },
                        },
                    ],
                }

            return {
                "role": "assistant",
                "content": message.content or "",
            }

        if message.role == LLMMessageRole.TOOL:
            if message.tool_result is None:
                raise ValueError(
                    "Tool message requires a tool result."
                )

            return {
                "role": "tool",
                "content": message.tool_result.output,
                "tool_call_id": message.tool_result.call_id,
            }

        raise ValueError(
            f"Unsupported LLM message role: {message.role}"
        )