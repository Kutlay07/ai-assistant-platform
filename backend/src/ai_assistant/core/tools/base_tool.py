from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any


class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def parameters(self) -> Mapping[str, Any]:
        pass

    @abstractmethod
    def execute(
        self,
        arguments: Mapping[str, Any],
    ) -> str:
        pass