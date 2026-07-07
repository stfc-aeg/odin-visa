import asyncio
from collections.abc import Sequence

import structlog
from pyvisa import VisaIOError
from pyvisa.resources import MessageBasedResource

from odin_visa.devices.device import DeviceError

logger = structlog.get_logger()


class DeviceWriteError(DeviceError):
    def __init__(self, cmd: str) -> None:
        super().__init__(f"Failed to write `{cmd}` to device")


class DeviceReadError(DeviceError):
    def __init__(self) -> None:
        super().__init__("Failed to read response from device")


class K2470Transport:
    def __init__(self, device: MessageBasedResource) -> None:
        self.device = device
        self._lock = asyncio.Lock()

    async def write(self, cmd: str) -> None:
        async with self._lock:
            # TODO: Device error handling?
            try:
                await asyncio.to_thread(self.device.write, cmd)
            except VisaIOError as e:
                raise DeviceWriteError(cmd) from e

    async def query(self, cmd: str) -> str:
        async with self._lock:
            # TODO: Device error handling?
            return await asyncio.to_thread(self._query_blocking, cmd)

    def _query_blocking(self, cmd: str) -> str:
        try:
            self.device.write(cmd)
        except VisaIOError as e:
            raise DeviceWriteError(cmd) from e

        try:
            return self.device.read().strip()
        except VisaIOError as e:
            raise DeviceReadError from e

    async def query_bytes(self, cmd: str, data_points: int) -> Sequence[float]:
        async with self._lock:
            return await asyncio.to_thread(self._query_bytes_blocking, cmd, data_points)

    def _query_bytes_blocking(self, cmd: str, data_points: int) -> Sequence[float]:
        try:
            self.device.write(cmd)
        except VisaIOError as e:
            raise DeviceWriteError(cmd) from e

        try:
            return self.device.read_binary_values(datatype="d", data_points=data_points)
        except (VisaIOError, ValueError) as e:
            raise DeviceReadError from e
