import asyncio
from collections.abc import Sequence

import structlog
from pyvisa import VisaIOError
from pyvisa.resources import MessageBasedResource

from odin_visa.devices.device import DeviceError
from odin_visa.devices.keithley2470.types import Event, EventType

logger = structlog.get_logger()


class DeviceWriteError(DeviceError):
    def __init__(self, cmd: str) -> None:
        super().__init__(f"Failed to write `{cmd}` to device")


class DeviceReadError(DeviceError):
    def __init__(self) -> None:
        super().__init__("Failed to read response from device")


class DeviceMiscError(DeviceError):
    def __init__(self, messages: list[Event]) -> None:
        self.messages = messages
        super().__init__(f"Device Error Log contains: `{messages}`")


class StatusRequestBits:
    ERROR_AVAILIBLE = 1 << 2
    MESSAGE_AVAILIBLE = 1 << 4


class K2470Transport:
    def __init__(self, device: MessageBasedResource) -> None:
        self.device = device
        self._lock = asyncio.Lock()

    async def initialise(self) -> None:
        async with self._lock:
            await asyncio.to_thread(self._initialise_blocking)

    def _initialise_blocking(self) -> None:
        self.device.write("*RST")
        self.device.write(":SYST:CLE")
        self.device.write("FORM REAL")

    async def write(self, cmd: str) -> None:
        async with self._lock:
            await asyncio.to_thread(self._write_blocking, cmd)

    def _write_blocking(self, cmd: str) -> None:
        try:
            self.device.write(cmd)
            self._check_error_log()
        except VisaIOError as e:
            raise DeviceWriteError(cmd) from e

    async def query(self, cmd: str) -> str:
        async with self._lock:
            return await asyncio.to_thread(self._query_blocking, cmd)

    def _query_blocking(self, cmd: str) -> str:
        try:
            self.device.write(cmd)
            self._check_error_log()
        except (VisaIOError, DeviceMiscError) as e:
            raise DeviceWriteError(cmd) from e

        try:
            ret = self.device.read().strip()
            self._check_error_log()
        except VisaIOError as e:
            raise DeviceReadError from e
        else:
            return ret

    async def query_bytes(self, cmd: str, data_points: int) -> Sequence[float]:
        async with self._lock:
            return await asyncio.to_thread(self._query_bytes_blocking, cmd, data_points)

    def _query_bytes_blocking(self, cmd: str, data_points: int) -> Sequence[float]:
        try:
            self.device.write(cmd)
            self._check_error_log()
        except VisaIOError as e:
            raise DeviceWriteError(cmd) from e

        try:
            ret = self.device.read_binary_values(datatype="d", data_points=data_points)
            self._check_error_log()
        except (VisaIOError, ValueError) as e:
            raise DeviceReadError from e
        else:
            return ret

    def _check_error_log(self) -> None:
        errors = []
        while self.device.read_stb() & StatusRequestBits.ERROR_AVAILIBLE:
            response = self.device.query(":SYST:ERR:NEXT?")
            parsed = self._parse_error_message(response)
            errors.append(parsed)
            logger.warning("Device returned an error", error=parsed)
        if len(errors) != 0:
            raise DeviceMiscError(errors)

    def _parse_error_message(self, msg: str) -> Event:
        stripped = msg.strip().replace('"', "")
        comma_split = stripped.split(",", 1)
        semicolon_split = comma_split[1].split(";")
        return Event(
            code=int(comma_split[0]),
            message=semicolon_split[0],
            kind=EventType(int(semicolon_split[1])),
            datetime=semicolon_split[2],
        )
