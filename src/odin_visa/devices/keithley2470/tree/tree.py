import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.device_config import DeviceConfig
from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.util.instrument import instrument, instrument_async

from .buffer import BufferTree
from .config import ConfigTree

logger = structlog.get_logger()


class K2470Tree:
    @instrument(logger, skip={"state"})
    def __init__(
        self, state: K2470State, driver: K2470Driver, config: DeviceConfig
    ) -> None:
        self.state = state
        self.driver = driver

        self.config_tree = ConfigTree(state, driver)
        self.buffer_tree = BufferTree(state, driver, config)

        self.tree = AsyncParameterTree(
            {
                "config": self.config_tree.tree,
                "buffers": self.buffer_tree.tree,
                "ident": (lambda: self.state.ident, None),
                "address": (lambda: self.state.address, None),
                "type": (lambda: self.state.kind, None),
                "poll_freq": (
                    lambda: self.state.poll_freq,
                    lambda freq: setattr(self.state, "poll_freq", freq),
                ),
            }
        )

    @instrument_async(logger)
    async def set_from_state(self) -> None:
        await self.config_tree.set_from_state()

    @instrument_async(logger)
    async def refresh(self) -> None:
        await self.config_tree.refresh()
