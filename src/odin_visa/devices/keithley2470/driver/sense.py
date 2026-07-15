import structlog

from odin_visa.devices.keithley2470.driver._catch_error import catch_error
from odin_visa.devices.keithley2470.driver.error import InvalidResponseError
from odin_visa.devices.keithley2470.state import EventLogState
from odin_visa.devices.keithley2470.transport import K2470Transport
from odin_visa.devices.keithley2470.types import (
    AveragingType,
    SenseFunction,
)
from odin_visa.util.scpi_parse import parse_bool, parse_enum, parse_float, parse_int

logger = structlog.get_logger()


class SenseDriver:
    def __init__(self, transport: K2470Transport, event_log: EventLogState) -> None:
        self.transport = transport
        self.event_log = event_log
        self.function_cache = None

    @catch_error
    async def set_averaging_count(self, value: int) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:AVER:COUN {value}")

    @catch_error
    async def get_averaging_count(self) -> int:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:AVER:COUN?")
        try:
            return parse_int(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_averaging(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:AVER {value:d}")

    @catch_error
    async def get_averaging(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:AVER?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_auto_zero(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:AZER {value:d}")

    @catch_error
    async def get_auto_zero(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:AZER?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_averaging_filter(self, value: AveragingType) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:AVER:TCON {value}")

    @catch_error
    async def get_averaging_filter(self) -> AveragingType:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:AVER:TCON?")
        try:
            return parse_enum(response, AveragingType, match_start=True)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_nplcs(self, value: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:NPLC {value}")

    @catch_error
    async def get_nplcs(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:NPLC?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_offset_compensation(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:OCOM {value:d}")

    @catch_error
    async def get_offset_compensation(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:OCOM?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_auto_range(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:RANGE:AUTO {value:d}")

    @catch_error
    async def get_auto_range(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:RANGE:AUTO?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_auto_range_lower_limit(self, value: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:RANGE:AUTO:LLIM {value}")

    @catch_error
    async def get_auto_range_lower_limit(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:RANGE:AUTO:LLIM?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_auto_range_rebound(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:RANGE:AUTO:REB {value:d}")

    @catch_error
    async def get_auto_range_rebound(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:RANGE:AUTO:REB?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_auto_range_upper_limit(self, value: float) -> None:
        # Only used for resistence measurements (currently unimplemented)
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:RANGE:AUTO:ULIM {value}")

    @catch_error
    async def get_auto_range_upper_limit(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:RANGE:AUTO:ULIM?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_range(self, value: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:RANGE {value}")

    @catch_error
    async def get_range(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:RANGE?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_relative_offset_level(self, value: float) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:REL {value}")

    @catch_error
    async def get_relative_offset_level(self) -> float:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:REL?")
        try:
            return parse_float(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def acquire_relative_offset(self, _: None) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:REL:ACQ")

    @catch_error
    async def set_relative_offset(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:REL:STAT {value:d}")

    @catch_error
    async def get_relative_offset(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:REL:STAT?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_remote_sensing(self, value: bool) -> None:
        function = await self.get_function()
        await self.transport.write(f"SENS:{function}:RSEN {value:d}")

    @catch_error
    async def get_remote_sensing(self) -> bool:
        function = await self.get_function()
        response = await self.transport.query(f"SENS:{function}:RSEN?")
        try:
            return parse_bool(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def zero(self, _: None) -> None:
        await self.transport.write("SENS:AZER:ONCE")

    @catch_error
    async def set_count(self, value: int) -> None:
        await self.transport.write(f"SENS:COUN {value}")

    @catch_error
    async def get_count(self) -> int:
        response = await self.transport.query("SENS:COUN?")
        try:
            return parse_int(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @catch_error
    async def set_function(self, function: SenseFunction) -> None:
        await self.transport.write(f'SENS:FUNC "{function}"')

    @catch_error
    async def get_function(self) -> SenseFunction:
        if self.function_cache is not None:
            return self.function_cache

        logger.debug("SenseFunction cache stale, refetching")
        response = await self.transport.query("SENS:FUNC?")
        response = response.strip('"')
        response = response.rstrip(":DC")
        try:
            self.function_cache = parse_enum(response, SenseFunction, match_start=True)
        except ValueError as e:
            raise InvalidResponseError(response) from e
        return self.function_cache

    def invalidate_function_cache(self) -> None:
        self.function_cache = None
