import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.util.instrument import instrument_async

logger = structlog.get_logger()


class SenseTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state.config.sense
        self.driver = driver.sense
        self.tree = AsyncParameterTree(
            {
                "averaging_count": (
                    lambda: self.state.averaging_count,
                    self.driver.set_averaging_count,
                ),
                "averaging": (
                    lambda: self.state.averaging_enable,
                    self.driver.set_averaging,
                ),
                "averaging_filter": (
                    lambda: str(self.state.averaging_type),
                    self.driver.set_averaging_filter,
                ),
                "auto_zero": (
                    lambda: self.state.auto_zero,
                    self.driver.set_auto_zero,
                ),
                "nplcs": (
                    lambda: self.state.nplcs,
                    self.driver.set_nplcs,
                ),
                "offset_compensation": (
                    lambda: self.state.offset_compensation,
                    self.driver.set_offset_compensation,
                ),
                "auto_range": (
                    lambda: self.state.auto_range,
                    self.driver.set_auto_range,
                ),
                "auto_range_lower_limit": (
                    lambda: self.state.auto_range_lower_limit,
                    self.driver.set_auto_range_lower_limit,
                ),
                "auto_range_rebound": (
                    lambda: self.state.auto_range_rebound,
                    self.driver.set_auto_range_rebound,
                ),
                "auto_range_upper_limit": (
                    lambda: self.state.auto_range_lower_limit,
                    self.driver.set_auto_range_upper_limit,
                ),
                "range": (
                    lambda: self.state.range,
                    self.driver.set_range,
                ),
                "relative_offset_level": (
                    lambda: self.state.relative_offset_level,
                    self.driver.set_relative_offset_level,
                ),
                "acquire_relative_offset": (
                    None,
                    self.driver.acquire_relative_offset,
                ),
                "relative_offset": (
                    lambda: self.state.relative_offset,
                    self.driver.set_relative_offset,
                ),
                "remote_sensing": (
                    lambda: self.state.remote_sensing,
                    self.driver.set_remote_sensing,
                ),
                "zero": (None, self.driver.zero),
                "count": (lambda: self.state.count, self.driver.set_count),
                "function": (
                    lambda: str(self.state.function),
                    self.driver.set_function,
                ),
            }
        )

    @instrument_async(logger)
    async def set_from_state(self) -> None:
        await self.driver.set_function(self.state.function)
        await self.driver.set_count(self.state.count)
        await self.driver.set_averaging_count(self.state.averaging_count)
        await self.driver.set_averaging(self.state.averaging_enable)
        await self.driver.set_averaging_filter(self.state.averaging_type)
        await self.driver.set_auto_zero(self.state.auto_zero)
        await self.driver.set_nplcs(self.state.nplcs)
        await self.driver.set_offset_compensation(self.state.offset_compensation)
        await self.driver.set_auto_range(self.state.auto_range)
        await self.driver.set_auto_range_lower_limit(self.state.auto_range_lower_limit)
        await self.driver.set_auto_range_rebound(self.state.auto_range_rebound)
        await self.driver.set_range(self.state.range)
        await self.driver.set_relative_offset_level(self.state.relative_offset_level)
        await self.driver.set_relative_offset(self.state.relative_offset)
        await self.driver.set_remote_sensing(self.state.remote_sensing)

    @instrument_async(logger)
    async def refresh(self) -> None:
        self.state.function = await self.driver.get_function()
        self.state.count = await self.driver.get_count()
        self.state.averaging_count = await self.driver.get_averaging_count()
        self.state.averaging_enable = await self.driver.get_averaging()
        self.state.averaging_type = await self.driver.get_averaging_filter()
        self.state.auto_zero = await self.driver.get_auto_zero()
        self.state.nplcs = await self.driver.get_nplcs()
        self.state.offset_compensation = await self.driver.get_offset_compensation()
        self.state.auto_range = await self.driver.get_auto_range()
        self.state.auto_range_lower_limit = (
            await self.driver.get_auto_range_lower_limit()
        )
        self.state.auto_range_rebound = await self.driver.get_auto_range_rebound()
        self.state.auto_range_upper_limit = (
            await self.driver.get_auto_range_upper_limit()
        )
        self.state.range = await self.driver.get_range()
        self.state.relative_offset_level = await self.driver.get_relative_offset_level()
        self.state.relative_offset = await self.driver.get_relative_offset()
        self.state.remote_sensing = await self.driver.get_remote_sensing()
