import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State

logger = structlog.get_logger()


class SenseTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state.config.sense
        self.driver = driver
        self.tree = AsyncParameterTree(
            {
                "averaging_count": (
                    lambda: self.state.averaging_count,
                    self.driver.sense.set_averaging_count,
                ),
                "averaging": (
                    lambda: self.state.averaging,
                    self.driver.sense.set_averaging,
                ),
                "averaging_filter": (
                    lambda: str(self.state.averaging_type),
                    self.driver.sense.set_averaging_filter,
                ),
                "auto_zero": (
                    lambda: self.state.auto_zero,
                    self.driver.sense.set_auto_zero,
                ),
                "nplcs": (
                    lambda: self.state.nplcs,
                    self.driver.sense.set_nplcs,
                ),
                "offset_compensation": (
                    lambda: self.state.offset_compensation,
                    self.driver.sense.set_offset_compensation,
                ),
                "auto_range": (
                    lambda: self.state.auto_range,
                    self.driver.sense.set_auto_range,
                ),
                "auto_range_lower_limit": (
                    lambda: self.state.auto_range_lower_limit,
                    self.driver.sense.set_auto_range_lower_limit,
                ),
                "auto_range_rebound": (
                    lambda: self.state.auto_range_rebound,
                    self.driver.sense.set_auto_range_rebound,
                ),
                "auto_range_upper_limit": (
                    lambda: self.state.auto_range_lower_limit,
                    self.driver.sense.set_auto_range_upper_limit,
                ),
                "range": (
                    lambda: self.state.range,
                    self.driver.sense.set_range,
                ),
                "relative_offset_level": (
                    lambda: self.state.relative_offset_level,
                    self.driver.sense.set_relative_offset_level,
                ),
                "acquire_relative_offset": (
                    None,
                    self.driver.sense.acquire_relative_offset,
                ),
                "relative_offset": (
                    lambda: self.state.relative_offset,
                    self.driver.sense.set_relative_offset,
                ),
                "remote_sensing": (
                    lambda: self.state.remote_sensing,
                    self.driver.sense.set_remote_sensing,
                ),
                "zero": (None, self.driver.sense.zero),
                "count": (lambda: self.state.count, self.driver.sense.set_count),
                "function": (
                    lambda: str(self.state.function),
                    self.driver.sense.set_function,
                ),
            }
        )

    async def set_from_state(self) -> None:
        await self.driver.sense.set_function(self.state.function)
        await self.driver.sense.set_count(self.state.count)
        await self.driver.sense.set_averaging_count(self.state.averaging_count)
        await self.driver.sense.set_averaging(self.state.averaging)
        await self.driver.sense.set_averaging_filter(self.state.averaging_type)
        await self.driver.sense.set_auto_zero(self.state.auto_zero)
        await self.driver.sense.set_nplcs(self.state.nplcs)
        await self.driver.sense.set_offset_compensation(self.state.offset_compensation)
        await self.driver.sense.set_auto_range(self.state.auto_range)
        await self.driver.sense.set_auto_range_lower_limit(
            self.state.auto_range_lower_limit
        )
        await self.driver.sense.set_auto_range_rebound(self.state.auto_range_rebound)
        await self.driver.sense.set_range(self.state.range)
        await self.driver.sense.set_relative_offset_level(
            self.state.relative_offset_level
        )
        await self.driver.sense.set_relative_offset(self.state.relative_offset)
        await self.driver.sense.set_remote_sensing(self.state.remote_sensing)

    async def refresh(self) -> None:
        self.driver.sense.invalidate_function_cache()
        function = await self.driver.sense.get_function()
        self.state.function = function

        (
            self.state.count,
            self.state.averaging_count,
            self.state.averaging,
            self.state.averaging_type,
            self.state.auto_zero,
            self.state.nplcs,
            self.state.offset_compensation,
            self.state.auto_range,
            self.state.auto_range_lower_limit,
            self.state.auto_range_rebound,
            self.state.auto_range_upper_limit,
            self.state.range,
            self.state.relative_offset_level,
            self.state.relative_offset,
            self.state.remote_sensing,
        ) = await self.driver.execute(
            [
                self.driver.sense.get_count(),
                self.driver.sense.get_averaging_count(function),
                self.driver.sense.get_averaging(function),
                self.driver.sense.get_averaging_filter(function),
                self.driver.sense.get_auto_zero(function),
                self.driver.sense.get_nplcs(function),
                self.driver.sense.get_offset_compensation(function),
                self.driver.sense.get_auto_range(function),
                self.driver.sense.get_auto_range_lower_limit(function),
                self.driver.sense.get_auto_range_rebound(function),
                self.driver.sense.get_auto_range_upper_limit(function),
                self.driver.sense.get_range(function),
                self.driver.sense.get_relative_offset_level(function),
                self.driver.sense.get_relative_offset(function),
                self.driver.sense.get_remote_sensing(function),
            ]
        )
