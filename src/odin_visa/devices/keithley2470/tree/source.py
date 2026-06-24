import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.util.instrument import instrument

logger = structlog.get_logger()


class SourceTree:
    @instrument(logger, skip={"state"})
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state.config.source
        self.driver = driver.source
        self.tree = AsyncParameterTree(
            {
                "function": (
                    lambda: str(self.state.function),
                    self.driver.set_function,
                ),
                "level": (
                    lambda: self.state.level,
                    self.driver.set_level,
                ),
                "limit": (
                    lambda: self.state.limit,
                    self.driver.set_limit,
                ),
            }
        )

    @instrument(logger)
    async def set_from_state(self) -> None:
        await self.driver.set_function(self.state.function)
        await self.driver.set_level(self.state.level)
        await self.driver.set_limit(self.state.limit)

    @instrument(logger)
    async def refresh(self) -> None:
        self.state.function = await self.driver.get_function()
        self.state.level = await self.driver.get_level(self.state.function)
        self.state.level = await self.driver.get_level(self.state.function)
