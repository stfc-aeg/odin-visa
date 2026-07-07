from odin_visa.devices.keithley2470.driver.error import InvalidResponseError
from odin_visa.devices.keithley2470.state import SMode, Terminal
from odin_visa.devices.keithley2470.transport import K2470Transport
from odin_visa.devices.keithley2470.types import SourceFunction
from odin_visa.util.scpi_parse import parse_bool, parse_enum


class OutputDriver:
    def __init__(self, transport: K2470Transport) -> None:
        self.transport = transport

    async def set_smode(self, value: SMode) -> None:
        function = await self.get_function()
        await self.transport.write(f"OUTP:{function}:SMODE {value}")

    async def get_smode(self) -> SMode:
        function = await self.get_function()
        response = await self.transport.query(f"OUTP:{function}:SMODE?")
        try:
            return parse_enum(response, SMode, match_start=True)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_interlock(self, value: bool) -> None:
        await self.transport.write(f"OUTP:INTERLOCK:STATE {int(value)}")

    async def get_interlock(self) -> bool:
        response = await self.transport.query("OUTP:INTERLOCK:STATE?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def get_interlock_tripped(self) -> bool:
        response = await self.transport.query("OUTP:INTERLOCK:TRIP?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_enabled(self, value: bool) -> None:
        await self.transport.write(f"OUTP {int(value)}")

    async def get_enabled(self) -> bool:
        response = await self.transport.query("OUTP?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_terminals(self, value: Terminal) -> None:
        await self.transport.write(f"ROUT:TERM {value}")

    async def get_terminals(self) -> Terminal:
        response = await self.transport.query("ROUT:TERM?")
        try:
            return parse_enum(response, Terminal, match_start=True)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def get_function(self) -> SourceFunction:
        response = await self.transport.query("SOUR:FUNC?")
        try:
            return parse_enum(response, SourceFunction, match_start=True)
        except ValueError as e:
            raise InvalidResponseError(response) from e
