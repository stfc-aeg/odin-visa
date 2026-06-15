from pathlib import Path
from datetime import datetime, timezone
from typing import TYPE_CHECKING
from odin_visa.tree import Leaf, ParameterTreeMixin

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class SaveFileConfigTree(ParameterTreeMixin):
    def __init__(self, device: "K2470Device", base_folder: str):
        self._device = device
        self.base_folder = base_folder

        self.file = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')}.hdf5"
        self.subfolder = ""
        self.path = self.get_path()

    def update(self):
        pass

    def set_file(self, file: str):
        self.file = file

    def set_subfolder(self, subfolder: str):
        self.subfolder = subfolder

    def get_path(self):
        file = self.file
        if not file.endswith(".hdf5") and not file.endswith(".h5"):
            file += ".hdf5"

        path = Path(self.base_folder).joinpath(self.subfolder).joinpath(file)
        return str(path)

    file = Leaf(str, set=set_file)
    subfolder = Leaf(str, set=set_subfolder)
    path = Leaf(str, get_path)
