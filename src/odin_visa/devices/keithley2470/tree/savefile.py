from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.state import K2470State, SaveFileConfigState


class SaveFileTree:
    def __init__(self, state: K2470State) -> None:
        self.state = state.config.savefile
        self.tree = AsyncParameterTree(
            {
                "enable": (lambda: self.state.enable, self._set_enable),
                "set_file_from_timestamp": (None, self._set_file_from_timestamp),
                "file": (lambda: self.state.file, self._set_file),
                "subfolder": (lambda: self.state.subfolder, self._set_subfolder),
                "full_path": (lambda: str(self.state.path()), None),
                "exists": (lambda: self.state.path().exists(), None),
            }
        )

    def _set_enable(self, value: bool) -> None:
        self.state.enable = value

    def _set_file(self, value: str) -> None:
        self.state.file = value

    def _set_subfolder(self, value: str) -> None:
        self.state.subfolder = value

    def _set_file_from_timestamp(self, _: None) -> None:
        self.state.file = SaveFileConfigState.timestamped_filename()
