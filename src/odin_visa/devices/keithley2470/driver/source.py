from asyncio import Transport
import logging
from odin_visa.util.scpi_parse import parse_enum, parse_float
from .error import DriverError
from ..transport import K2470Transport, TransportError
from ..types import SourceFunction


class SourceDriver:
    def __init__(self, transport: K2470Transport):
        self.transport = transport

    async def set_function(self, function: SourceFunction):
        logging.debug(f"source.set_function({function})")
        try:
            await self.transport.write(f"SOUR:FUNC {function}")
        except TransportError as e:
            raise DriverError(f"Failed to set `{function}` as source function") from e

    async def get_function(self) -> SourceFunction:
        logging.debug("source.get_function()")
        try:
            return parse_enum(await self.transport.query("SOUR:FUNC?"), SourceFunction)
        except (TransportError, ValueError) as e:
            raise DriverError("Failed to get source function") from e

    async def set_level(self, level: float):
        logging.debug(f"source.set_level({level})")
        try:
            function = await self.get_function()
            await self.transport.write(f"SOUR:{function} {level}")
        except (DriverError, TransportError, ValueError) as e:
            raise DriverError(f"Failed to set `{level}` as source level") from e

    async def get_level(self, function: SourceFunction) -> float:
        logging.debug("source.get_level()")
        try:
            return parse_float(await self.transport.query(f"SOUR:{function}?"))
        except (TransportError, ValueError) as e:
            raise DriverError("Failed to get source level") from e

    async def set_limit(self, limit: float):
        logging.debug(f"source.set_limit({limit})")
        try:
            function = await self.get_function()
            await self.transport.write(
                f"SOUR:{function}:{self._limiting_function(function)}LIM {limit}"
            )
        except (TransportError, ValueError, DriverError) as e:
            raise DriverError(f"Failed to set `{limit}` as source limit") from e

    async def get_limit(self, function: SourceFunction) -> float:
        logging.debug("source.get_limit()")
        try:
            return parse_float(
                await self.transport.query(
                    f"SOUR:{function}:{self._limiting_function(function)}LIM?"
                )
            )
        except (TransportError, ValueError) as e:
            raise DriverError("Failed to get source limit") from e

    @staticmethod
    def _limiting_function(function: SourceFunction) -> str:
        match function:
            case SourceFunction.CURRENT:
                return "V"
            case SourceFunction.VOLTAGE:
                return "I"
