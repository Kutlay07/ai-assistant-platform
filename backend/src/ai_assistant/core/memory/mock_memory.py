from .base_memory import BaseMemory


class MockMemory(BaseMemory):

    def __init__(self):
        self._messages = []
        self._summary = None


    def get_history(self) -> list[dict[str, str]]:
        return self._messages.copy()


    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        self._messages.append(
            {
                "role": role,
                "content": content,
            }
        )


    def get_summary(self) -> str | None:
        return self._summary


    def save_summary(
        self,
        summary: str,
    ) -> None:
        self._summary = summary
        
        
    def replace_history(
        self,
        history: list[dict[str, str]],
    ) -> None:
        self._messages = history.copy()