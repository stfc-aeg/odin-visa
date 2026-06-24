from odin_visa.util.instrument import instrument
import structlog

from odin_visa.devices.keithley2470.transport import K2470Transport
from odin_visa.devices.keithley2470.types import SourceFunction
from odin_visa.util.scpi_parse import parse_enum, parse_float

from .error import InvalidResponseError

logger = structlog.get_logger()


class SourceDriver:
    def __init__(self, transport: K2470Transport) -> None:
        self.transport = transport

    @instrument(logger)
    async def set_function(self, function: SourceFunction) -> None:
        await self.transport.write(f"SOUR:FUNC {function}")

    @instrument(logger)
    async def get_function(self) -> SourceFunction:
        response = await self.transport.query("SOUR:FUNC?")
        try:
            return parse_enum(response, SourceFunction)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @instrument(logger)
    async def set_level(self, level: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function} {level}")

    @instrument(logger)
    async def get_level(self, function: SourceFunction) -> float:
        response = await self.transport.query(f"SOUR:{function}?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @instrument(logger)
    async def set_limit(self, limit: float) -> None:
        function = await self.get_function()
        await self.transport.write(
            f"SOUR:{function}:{self._limiting_function(function)}LIM {limit}"
        )

    @instrument(logger)
    async def get_limit(self, function: SourceFunction) -> float:
        response = await self.transport.query(
            f"SOUR:{function}:{self._limiting_function(function)}LIM?"
        )
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @staticmethod
    def _limiting_function(function: SourceFunction) -> str:
        match function:
            case SourceFunction.CURRENT:
                return "V"
            case SourceFunction.VOLTAGE:
                return "I"
