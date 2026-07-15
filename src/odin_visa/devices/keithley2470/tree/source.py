import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.util.instrument import instrument

logger = structlog.get_logger()


class SourceTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state.config.source
        self.driver = driver.source
        self.tree = AsyncParameterTree(
            {
                "delay": (
                    lambda: self.state.delay,
                    self.driver.set_delay,
                ),
                "auto_delay": (
                    lambda: self.state.auto_delay,
                    self.driver.set_auto_delay,
                ),
                "high_capacitance": (
                    lambda: self.state.high_capacitance,
                    self.driver.set_high_capacitance,
                ),
                "level": (
                    lambda: self.state.level,
                    self.driver.set_level,
                ),
                "limit": (
                    lambda: self.state.limit,
                    self.driver.set_limit,
                ),
                "limit_tripped": (
                    lambda: self.state.limit_tripped,
                    lambda: None,
                ),
                "function": (
                    lambda: str(self.state.function),
                    self.driver.set_function,
                ),
                "protection": (
                    lambda: str(self.state.protection),
                    self.driver.set_protection_level,
                ),
                "protection_tripped": (
                    lambda: self.state.protection_tripped,
                    None,
                ),
                "range": (
                    lambda: self.state.range,
                    self.driver.set_range,
                ),
                "auto_range": (
                    lambda: self.state.auto_range,
                    self.driver.set_auto_range,
                ),
                "read_back": (
                    lambda: self.state.read_back,
                    self.driver.set_read_back,
                ),
            }
        )

    async def set_from_state(self) -> None:
        await self.driver.set_delay(self.state.delay)
        await self.driver.set_auto_delay(self.state.auto_delay)
        await self.driver.set_high_capacitance(self.state.high_capacitance)
        await self.driver.set_level(self.state.level)
        await self.driver.set_limit(self.state.limit)
        await self.driver.set_function(self.state.function)
        await self.driver.set_protection_level(self.state.protection)
        await self.driver.set_range(self.state.range)
        await self.driver.set_auto_range(self.state.auto_range)
        await self.driver.set_read_back(self.state.read_back)

    async def refresh(self) -> None:
        self.driver.invalidate_function_cache()

        self.state.delay = await self.driver.get_delay()
        self.state.auto_delay = await self.driver.get_auto_delay()
        self.state.high_capacitance = await self.driver.get_high_capacitance()
        self.state.level = await self.driver.get_level()
        self.state.limit = await self.driver.get_limit()
        self.state.limit_tripped = await self.driver.get_limit_tripped()
        self.state.function = await self.driver.get_function()
        self.state.protection = await self.driver.get_protection_level()
        self.state.protection_tripped = await self.driver.get_protection_tripped()
        self.state.range = await self.driver.get_range()
        self.state.auto_range = await self.driver.get_auto_range()
        self.state.read_back = await self.driver.get_read_back()
