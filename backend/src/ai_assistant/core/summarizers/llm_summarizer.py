from collections.abc import Sequence

from ..llms import BaseLLM
from .base_summarizer import BaseSummarizer


class LLMSummarizer(BaseSummarizer):

    def __init__(
        self,
        llm: BaseLLM,
    ) -> None:
        self._llm = llm

    def summarize(
        self,
        messages: Sequence[dict[str, str]],
        previous_summary: str | None = None,
    ) -> str:

        messages_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in messages
        )

        prompt = self._build_prompt(
            messages_text=messages_text,
            previous_summary=previous_summary,
        )

        return self._llm.generate(prompt)

    def _build_prompt(
        self,
        messages_text: str,
        previous_summary: str | None,
    ) -> str:

        if previous_summary is None:
            return f"""Summarize the following conversation.

Preserve important facts, user preferences, decisions, goals, constraints, and relevant context.

Conversation:
{messages_text}

Summary:"""

        return f"""Update the existing conversation summary using the new conversation messages.

Preserve important information from the previous summary unless it is contradicted or no longer relevant.

Previous summary:
{previous_summary}

New conversation messages:
{messages_text}

Updated summary:"""