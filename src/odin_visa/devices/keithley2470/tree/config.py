import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State

from .source import SourceTree

logger = structlog.get_logger()


class ConfigTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        logger.debug("initialising Config")
        self.state = state
        self.driver = driver

        self.source_tree = SourceTree(state, driver)

        self.tree = AsyncParameterTree({"source": self.source_tree.tree})
        logger.debug("initialised ConfigTree")

    async def set_from_state(self) -> None:
        await self.source_tree.set_from_state()

    async def refresh(self) -> None:
        logger.debug("refreshing ConfigTree")
        await self.source_tree.refresh()
        logger.debug("refreshed ConfigTree")
