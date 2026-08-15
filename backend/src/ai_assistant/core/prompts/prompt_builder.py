from collections.abc import Sequence
from pathlib import Path

from ..models.request import Request
from ..models import Chunk


TEMPLATE_DIR = Path(__file__).parent / "templates"


class PromptBuilder:
    def _load_template(self, name: str) -> str:
        template_path = TEMPLATE_DIR / f"{name}.txt"

        with template_path.open(encoding="utf-8") as f:
            return f.read()

    def build(
        self,
        request: Request,
        history: Sequence[dict[str, str]],
        current_step: str | None = None,
        template: str = "chat",
        context: list[Chunk] | None = None,
        summary: str | None = None,
    ) -> str:
        template_text = self._load_template(template)

        history_text = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history
        )
        
        context_text = ""

        if context:
            context_text = "\n\n".join(
                f"[Chunk {i + 1}]\n{chunk.content}"
                for i, chunk in enumerate(context))

        return template_text.format(
            history=history_text,
            summary=summary or "",
            input=request.input,
            current_step=current_step or "",
            context=context_text,
        )