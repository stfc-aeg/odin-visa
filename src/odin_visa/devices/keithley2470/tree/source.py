from odin_control.adapters.async_parameter_tree import AsyncParameterTree
from returns.pipeline import is_successful
import logging
from ..state import K2470State
from ..driver import K2470Driver


class SourceTree:
    def __init__(self, state: K2470State, driver: K2470Driver):
        logging.debug("initialising SourceTree")

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
        logging.debug("initialised SourceTree")

    async def set_from_state(self):
        await self.driver.set_function(self.state.function)
        await self.driver.set_level(self.state.level)
        await self.driver.set_limit(self.state.limit)

    async def refresh(self):
        logging.debug("refreshing SourceTree")

        self.state.function = await self.driver.get_function()
        self.state.level = await self.driver.get_level(self.state.function)
        self.state.level = await self.driver.get_level(self.state.function)

        logging.debug("refreshed SourceTree")
