import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.managers.acquisition import Acquisition
from odin_visa.devices.keithley2470.state import K2470State

logger = structlog.get_logger()


class AcquisitionTree:
    def __init__(
        self, state: K2470State, driver: K2470Driver, acquisition: Acquisition
    ) -> None:
        self.state = state.config.acquisition
        self.driver = driver

        self.acquisition = acquisition
        self.acquiring = False

        self.tree = AsyncParameterTree(
            {
                "acquiring": (lambda: self.acquiring, self._set_acquiring),
            }
        )

    async def _set_acquiring(self, value: bool) -> None:
        if value:
            await self.acquisition.start_acquisition()
        else:
            await self.acquisition.stop_acquisition()

        self.acquiring = value

    async def set_from_state(self) -> None:
        await self._set_acquiring(self.state.acquiring)

    async def refresh(self) -> None:
        pass
