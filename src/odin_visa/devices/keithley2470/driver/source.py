import structlog

from odin_visa.devices.keithley2470.transport import K2470Transport
from odin_visa.devices.keithley2470.types import ProtectionLevel, SourceFunction
from odin_visa.util.instrument import instrument_async
from odin_visa.util.scpi_parse import parse_bool, parse_enum, parse_float

from .error import InvalidResponseError

logger = structlog.get_logger()


class SourceDriver:
    def __init__(self, transport: K2470Transport) -> None:
        self.transport = transport

    async def set_delay(self, delay: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:DELAY {delay}")

    async def get_delay(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}:DELAY?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_auto_delay(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:DELAY:AUTO {value:d}")

    async def get_auto_delay(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}:DELAY:AUTO?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_high_capacitance(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:HIGH:CAP {value:d}")

    async def get_high_capacitance(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}:HIGH:CAP?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_level(self, level: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function} {level}")

    async def get_level(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_limit(self, limit: float) -> None:
        function = await self.get_function()
        await self.transport.write(
            f"SOUR:{function}:{self._limiting_function(function)}LIM {limit}"
        )

    async def get_limit(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(
            f"SOUR:{function}:{self._limiting_function(function)}LIM?"
        )
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def get_limit_tripped(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(
            f"SOUR:{function}:{self._limiting_function(function)}LIM:TRIP?"
        )
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_function(self, function: SourceFunction) -> None:
        await self.transport.write(f"SOUR:FUNC {function}")

    async def get_function(self) -> SourceFunction:
        response = await self.transport.query("SOUR:FUNC?")
        try:
            return parse_enum(response, SourceFunction, match_start=True)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_protection_level(self, value: ProtectionLevel) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:PROT {value}")

    async def get_protection_level(self) -> ProtectionLevel:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}:PROT?")
        try:
            return parse_enum(response, ProtectionLevel)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def get_protection_tripped(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}:PROT:TRIP?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_range(self, value: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:RANGE {value}")

    async def get_range(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}:RANGE?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_auto_range(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:RANGE:AUTO {value:d}")

    async def get_auto_range(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}:RANGE:AUTO?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_read_back(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function}:READ:BACK {value:d}")

    async def get_read_back(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SOUR:{function}:READ:BACK?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    # TODO: sweeps?

    @staticmethod
    def _limiting_function(function: SourceFunction) -> str:
        match function:
            case SourceFunction.CURRENT:
                return "V"
            case SourceFunction.VOLTAGE:
                return "I"
