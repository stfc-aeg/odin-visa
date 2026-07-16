import structlog

from odin_visa.devices.keithley2470.driver._catch_error import catch_error
from odin_visa.devices.keithley2470.driver._query import SCPIQuery
from odin_visa.devices.keithley2470.state import EventLogState
from odin_visa.devices.keithley2470.transport import DeviceMiscError, K2470Transport
from odin_visa.devices.keithley2470.types import ProtectionLevel, SourceFunction
from odin_visa.util.scpi_parse import parse_bool, parse_enum, parse_float

from .error import InvalidResponseError

logger = structlog.get_logger()


class SourceDriver:
    def __init__(self, transport: K2470Transport, event_log: EventLogState) -> None:
        self.transport = transport
        self.event_log = event_log
        self.function_cache = None

        self.tmp = 0

    @catch_error
    async def set_delay(self, delay: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:DELAY {delay}")

    def get_delay(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(query=f":SOUR:{function}:DELAY?", parser=parse_float)

    @catch_error
    async def set_auto_delay(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:DELAY:AUTO {value:d}")

    def get_auto_delay(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(query=f":SOUR:{function}:DELAY:AUTO?", parser=parse_bool)

    @catch_error
    async def set_high_capacitance(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:HIGH:CAP {value:d}")

    def get_high_capacitance(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(query=f":SOUR:{function}:HIGH:CAP?", parser=parse_bool)

    @catch_error
    async def set_level(self, level: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function} {level}")

    def get_level(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(query=f":SOUR:{function}?", parser=parse_float)

    @catch_error
    async def set_limit(self, limit: float) -> None:
        function = await self.get_function()
        await self.transport.write(
            f"SOUR:{function}:{self._limiting_function(function)}LIM {limit}"
        )

    def get_limit(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(
            query=f":SOUR:{function}:{self._limiting_function(function)}LIM?",
            parser=parse_float,
        )

    def get_limit_tripped(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(
            query=f":SOUR:{function}:{self._limiting_function(function)}LIM:TRIP?",
            parser=parse_bool,
        )

    @catch_error
    async def set_function(self, function: SourceFunction) -> None:
        await self.transport.write(f"SOUR:FUNC {function}")

    @catch_error
    async def get_function(self) -> SourceFunction:
        if self.function_cache is not None:
            return self.function_cache

        logger.debug("SourceFunction cache stale, refetching")
        response = await self.transport.query("SOUR:FUNC?")
        try:
            self.function_cache = parse_enum(response, SourceFunction, match_start=True)
        except ValueError as e:
            raise InvalidResponseError(response) from e
        return self.function_cache

    def invalidate_function_cache(self) -> None:
        self.function_cache = None

    @catch_error
    async def set_protection_level(self, value: ProtectionLevel) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:PROT {value}")

    def get_protection_level(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(
            query=f":SOUR:{function}:PROT?",
            parser=lambda response: parse_enum(response, ProtectionLevel),
        )

    def get_protection_tripped(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(query=f":SOUR:{function}:PROT:TRIP?", parser=parse_bool)

    @catch_error
    async def set_range(self, value: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:RANGE {value}")

    def get_range(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(query=f":SOUR:{function}:RANGE?", parser=parse_float)

    @catch_error
    async def set_auto_range(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:RANGE:AUTO {value:d}")

    def get_auto_range(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(query=f":SOUR:{function}:RANGE:AUTO?", parser=parse_bool)

    @catch_error
    async def set_read_back(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:READ:BACK {value:d}")

    def get_read_back(self, function: SourceFunction) -> SCPIQuery:
        return SCPIQuery(query=f":SOUR:{function}:READ:BACK?", parser=parse_bool)

    # TODO: sweeps?

    @staticmethod
    def _limiting_function(function: SourceFunction) -> str:
        match function:
            case SourceFunction.CURRENT:
                return "V"
            case SourceFunction.VOLTAGE:
                return "I"
