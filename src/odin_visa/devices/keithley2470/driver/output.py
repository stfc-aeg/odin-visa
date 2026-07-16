from odin_visa.devices.keithley2470.driver._catch_error import catch_error
from odin_visa.devices.keithley2470.driver._query import SCPIQuery
from odin_visa.devices.keithley2470.driver.error import InvalidResponseError
from odin_visa.devices.keithley2470.state import EventLogState, SMode, Terminal
from odin_visa.devices.keithley2470.transport import K2470Transport
from odin_visa.devices.keithley2470.types import SourceFunction
from odin_visa.util.scpi_parse import parse_bool, parse_enum


class OutputDriver:
    def __init__(self, transport: K2470Transport, event_log: EventLogState) -> None:
        self.transport = transport
        self.event_log = event_log

    @catch_error
    async def set_smode(self, value: SMode) -> None:
        function = await self.get_function()
        await self.transport.write(f"OUTP:{function}:SMODE {value}")

    def get_smode(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(
            query=f":OUTP:{function}:SMODE?",
            parser=lambda response: parse_enum(response, SMode, match_start=True),
        )

    @catch_error
    async def set_interlock(self, value: bool) -> None:
        await self.transport.write(f"OUTP:INTERLOCK:STATE {int(value)}")

    def get_interlock(self) -> SCPIQuery:
        return SCPIQuery(query=":OUTP:INTERLOCK:STATE?", parser=parse_bool)

    def get_interlock_tripped(self) -> SCPIQuery:
        return SCPIQuery(query=":OUTP:INTERLOCK:TRIP?", parser=parse_bool)

    @catch_error
    async def set_enabled(self, value: bool) -> None:
        await self.transport.write(f"OUTP {int(value)}")

    def get_enabled(self) -> SCPIQuery:
        return SCPIQuery(query=":OUTP?", parser=parse_bool)

    @catch_error
    async def set_terminals(self, value: Terminal) -> None:
        await self.transport.write(f"ROUT:TERM {value}")

    def get_terminals(self) -> SCPIQuery:
        return SCPIQuery(
            query=":ROUT:TERM?",
            parser=lambda response: parse_enum(response, Terminal, match_start=True),
        )

    @catch_error
    async def get_function(self) -> SourceFunction:
        response = await self.transport.query("SOUR:FUNC?")
        try:
            return parse_enum(response, SourceFunction, match_start=True)
        except ValueError as e:
            raise InvalidResponseError(response) from e
