from abc import ABC, abstractmethod

from odin_control.adapters.async_parameter_tree import AsyncParameterTree


class DeviceError(Exception):
    """Base exception for any error coming from the device."""


class Device(ABC):
    @abstractmethod
    def get_param_tree(self) -> AsyncParameterTree:
        pass

    @abstractmethod
    async def refresh_param_tree(self) -> None:
        pass

    @abstractmethod
    async def update_task(self) -> None:
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        pass
