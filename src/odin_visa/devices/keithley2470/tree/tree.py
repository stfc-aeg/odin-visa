import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.managers.acquisition import Acquisition
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.devices.keithley2470.tree.event_log import EventLogTree

from .buffer import BufferTree
from .config import ConfigTree

logger = structlog.get_logger()


class K2470Tree:
    def __init__(
        self,
        state: K2470State,
        driver: K2470Driver,
        acquisition: Acquisition,
    ) -> None:
        self.state = state
        self.driver = driver

        self.config_tree = ConfigTree(state, driver, acquisition)
        self.buffer_tree = BufferTree(state, driver)
        self.event_log_tree = EventLogTree(state)

        self.device_tree = AsyncParameterTree(
            {
                "ident": (lambda: self.state.ident, None),
                "address": (lambda: self.state.address, None),
                "type": (lambda: self.state.kind, None),
            }
        )

        self.tree = AsyncParameterTree(
            {
                "config": self.config_tree.tree,
                "buffer": self.buffer_tree.tree,
                "device": self.device_tree,
                "event_log": self.event_log_tree.tree,
            }
        )

    async def set_from_state(self) -> None:
        await self.config_tree.set_from_state()

    async def refresh(self) -> None:
        await self.config_tree.refresh()
