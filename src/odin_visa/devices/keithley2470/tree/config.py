import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.managers.acquisition import Acquisition
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.devices.keithley2470.tree.acquisition import AcquisitionTree
from odin_visa.devices.keithley2470.tree.output import OutputTree
from odin_visa.devices.keithley2470.tree.savefile import SaveFileTree
from odin_visa.util.instrument import instrument

from .sense import SenseTree
from .source import SourceTree

logger = structlog.get_logger()


class ConfigTree:
    @instrument(logger, skip={"state"})
    def __init__(
        self, state: K2470State, driver: K2470Driver, acquisition: Acquisition
    ) -> None:
        self.state = state
        self.driver = driver

        self.savefile_tree = SaveFileTree(state)
        self.source_tree = SourceTree(state, driver)
        self.sense_tree = SenseTree(state, driver)
        self.acquisition_tree = AcquisitionTree(state, driver, acquisition)
        self.output_tree = OutputTree(state, driver)

        self.tree = AsyncParameterTree(
            {
                "savefile": self.savefile_tree.tree,
                "source": self.source_tree.tree,
                "sense": self.sense_tree.tree,
                "acquisition": self.acquisition_tree.tree,
                "output": self.output_tree.tree,
                "poll_freq": (
                    lambda: self.state.poll_freq,
                    lambda freq: setattr(self.state, "poll_freq", freq),
                ),
            }
        )

    async def set_from_state(self) -> None:
        await self.source_tree.set_from_state()
        await self.sense_tree.set_from_state()
        await self.output_tree.set_from_state()
        await self.acquisition_tree.set_from_state()

    async def refresh(self) -> None:
        await self.source_tree.refresh()
        await self.sense_tree.refresh()
        await self.output_tree.refresh()
        await self.acquisition_tree.refresh()
