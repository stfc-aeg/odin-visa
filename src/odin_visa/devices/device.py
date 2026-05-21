from abc import ABC, abstractmethod

from odin_visa.tree import ParameterTreeMixin
from odin_visa.types import StrEnum


class Device(ParameterTreeMixin, ABC):
    @abstractmethod
    def query(self, cmd: str) -> str | None:
        pass

    @abstractmethod
    def write(self, cmd: str) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass
