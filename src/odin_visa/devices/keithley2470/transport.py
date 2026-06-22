import asyncio
from timeit import default_timer

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
            start = default_timer()

            # TODO: Device error handling?
            try:
                await asyncio.to_thread(self.device.write, cmd)
            except VisaIOError as e:
                raise DeviceWriteError(cmd) from e

            end = default_timer()
            duration = (end - start) * 1_000_000
            logger.debug("device write", cmd=cmd, duration_us=duration)

    async def query(self, cmd: str) -> str:
        async with self._lock:
            start = default_timer()

            # TODO: Device error handling?
            msg = await asyncio.to_thread(self._query_blocking, cmd)

            end = default_timer()
            duration = (end - start) * 1_000_000
            logger.debug(
                "device query",
                cmd=cmd,
                response=msg,
                duration_us=duration,
            )
            return msg

    def _query_blocking(self, cmd: str) -> str:
        try:
            self.device.write(cmd)
        except VisaIOError as e:
            raise DeviceWriteError(cmd) from e

        try:
            return self.device.read().strip()
        except VisaIOError as e:
            raise DeviceReadError from e
