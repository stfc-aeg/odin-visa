import structlog

from odin_visa.devices.keithley2470.transport import K2470Transport
from odin_visa.devices.keithley2470.types import SourceFunction
from odin_visa.util.scpi_parse import parse_enum, parse_float

from .error import InvalidResponseError

logger = structlog.get_logger()


class SourceDriver:
    def __init__(self, transport: K2470Transport) -> None:
        self.transport = transport

    async def set_function(self, function: SourceFunction) -> None:
        logger.debug("source.set_function(%s)", function)
        await self.transport.write(f"SOUR:FUNC {function}")

    async def get_function(self) -> SourceFunction:
        logger.debug("source.get_function()")
        response = await self.transport.query("SOUR:FUNC?")
        try:
            return parse_enum(response, SourceFunction)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_level(self, level: float) -> None:
        logger.debug("source.set_level(%f)", level)
        function = await self.get_function()
        await self.transport.write(f"SOUR:{function} {level}")

    async def get_level(self, function: SourceFunction) -> float:
        logger.debug("source.get_level()")
        response = await self.transport.query(f"SOUR:{function}?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def set_limit(self, limit: float) -> None:
        logger.debug("source.set_limit(%f)", limit)
        function = await self.get_function()
        await self.transport.write(
            f"SOUR:{function}:{self._limiting_function(function)}LIM {limit}"
        )

    async def get_limit(self, function: SourceFunction) -> float:
        logger.debug("source.get_limit()")
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
