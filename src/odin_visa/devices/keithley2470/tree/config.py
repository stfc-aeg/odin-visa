import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.devices.keithley2470.tree.savefile import SaveFileTree
from odin_visa.util.instrument import instrument

from .sense import SenseTree
from .source import SourceTree

logger = structlog.get_logger()


class ConfigTree:
    @instrument(logger, skip={"state"})
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state
        self.driver = driver

        self.savefile_tree = SaveFileTree(state)
        self.source_tree = SourceTree(state, driver)
        self.sense_tree = SenseTree(state, driver)

        self.tree = AsyncParameterTree(
            {
                "savefile": self.savefile_tree.tree,
                "source": self.source_tree.tree,
                "sense": self.sense_tree.tree,
                "poll_freq": (
                    lambda: self.state.poll_freq,
                    lambda freq: setattr(self.state, "poll_freq", freq),
                ),
            }
        )

    @instrument(logger)
    async def set_from_state(self) -> None:
        await self.source_tree.set_from_state()
        await self.sense_tree.set_from_state()

    @instrument(logger)
    async def refresh(self) -> None:
        await self.source_tree.refresh()
        await self.sense_tree.refresh()
