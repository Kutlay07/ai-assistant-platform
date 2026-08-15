from abc import ABC, abstractmethod


class BaseMemory(ABC):

    @abstractmethod
    def get_history(self) -> list[dict[str, str]]:
        pass

    @abstractmethod
    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:
        pass

    @abstractmethod
    def get_summary(self) -> str | None:
        pass

    @abstractmethod
    def save_summary(
        self,
        summary: str,
    ) -> None:
        pass

    @abstractmethod
    def replace_history(
        self,
        history: list[dict[str, str]],
    ) -> None:
        pass