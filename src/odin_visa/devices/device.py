from odin_control.adapters.async_parameter_tree import AsyncParameterTree
from abc import ABC, abstractmethod


class Device(ABC):
    @abstractmethod
    def get_param_tree(self) -> AsyncParameterTree:
        pass

    @abstractmethod
    async def refresh_param_tree(self):
        pass

    @abstractmethod
    async def update_task(self):
        pass
