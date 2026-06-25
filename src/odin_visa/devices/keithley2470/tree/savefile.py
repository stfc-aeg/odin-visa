from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.devices.keithley2470.transport import logger
from odin_visa.util.instrument import instrument


class SaveFileTree:
    @instrument(logger, skip={"state"})
    def __init__(self, state: K2470State) -> None:
        self.state = state.config.savefile
        self.tree = AsyncParameterTree(
            {
                "file": (lambda: self.state.file, self._set_file),
                "subfolder": (lambda: self.state.subfolder, self._set_subfolder),
                "full_path": (lambda: str(self.state.path()), None),
            }
        )

    def _set_file(self, value: str) -> None:
        self.state.file = value

    def _set_subfolder(self, value: str) -> None:
        self.state.subfolder = value
