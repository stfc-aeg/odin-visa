import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State

logger = structlog.get_logger()


class SourceTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state.config.source
        self.driver = driver
        self.tree = AsyncParameterTree(
            {
                "delay": (
                    lambda: self.state.delay,
                    self.driver.source.set_delay,
                ),
                "auto_delay": (
                    lambda: self.state.auto_delay,
                    self.driver.source.set_auto_delay,
                ),
                "high_capacitance": (
                    lambda: self.state.high_capacitance,
                    self.driver.source.set_high_capacitance,
                ),
                "level": (
                    lambda: self.state.level,
                    self.driver.source.set_level,
                ),
                "limit": (
                    lambda: self.state.limit,
                    self.driver.source.set_limit,
                ),
                "limit_tripped": (
                    lambda: self.state.limit_tripped,
                    lambda: None,
                ),
                "function": (
                    lambda: str(self.state.function),
                    self.driver.source.set_function,
                ),
                "protection": (
                    lambda: str(self.state.protection),
                    self.driver.source.set_protection_level,
                ),
                "protection_tripped": (
                    lambda: self.state.protection_tripped,
                    None,
                ),
                "range": (
                    lambda: self.state.range,
                    self.driver.source.set_range,
                ),
                "auto_range": (
                    lambda: self.state.auto_range,
                    self.driver.source.set_auto_range,
                ),
                "read_back": (
                    lambda: self.state.read_back,
                    self.driver.source.set_read_back,
                ),
            }
        )

    async def set_from_state(self) -> None:
        await self.driver.source.set_delay(self.state.delay)
        await self.driver.source.set_auto_delay(self.state.auto_delay)
        await self.driver.source.set_high_capacitance(self.state.high_capacitance)
        await self.driver.source.set_level(self.state.level)
        await self.driver.source.set_limit(self.state.limit)
        await self.driver.source.set_function(self.state.function)
        await self.driver.source.set_protection_level(self.state.protection)
        await self.driver.source.set_range(self.state.range)
        await self.driver.source.set_auto_range(self.state.auto_range)
        await self.driver.source.set_read_back(self.state.read_back)

    async def refresh(self) -> None:
        self.driver.source.invalidate_function_cache()
        function = await self.driver.source.get_function()

        (
            self.state.delay,
            self.state.auto_delay,
            self.state.high_capacitance,
            self.state.level,
            self.state.limit,
            self.state.limit_tripped,
            self.state.protection,
            self.state.protection_tripped,
            self.state.range,
            self.state.auto_range,
            self.state.read_back,
        ) = await self.driver.execute(
            [
                self.driver.source.get_delay(function),
                self.driver.source.get_auto_delay(function),
                self.driver.source.get_high_capacitance(function),
                self.driver.source.get_level(function),
                self.driver.source.get_limit(function),
                self.driver.source.get_limit_tripped(function),
                self.driver.source.get_protection_level(function),
                self.driver.source.get_protection_tripped(function),
                self.driver.source.get_range(function),
                self.driver.source.get_auto_range(function),
                self.driver.source.get_read_back(function),
            ]
        )
