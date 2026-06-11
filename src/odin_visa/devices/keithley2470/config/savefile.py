from datetime import datetime, timezone
from typing import TYPE_CHECKING
from odin_visa.tree import Leaf, ParameterTreeMixin

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class SaveFileConfig(ParameterTreeMixin):
    def __init__(self, device: "K2470Device"):
        self._device = device

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
        self.filepath = "test/acquisitions"
        self.filename = f"{timestamp}_k2470.hdf5"
        self.dataset_name = "acquisition"
        self.write_period = 5

    def set_filepath(self, filepath: str):
        self.filepath = filepath

    def set_filename(self, filename: str):
        self.filename = filename

    def set_dataset_name(self, dataset_name: str):
        self.dataset_name = dataset_name

    def set_write_period(self, period: int):
        self.write_period = period

    def update(self):
        pass

    """Name of the h5 file to write to"""
    filepath = Leaf(str, set=set_filepath)
    """Name of the h5 file to write to"""
    filename = Leaf(str, set=set_filename)
    """Name of the h5 dataset to create within the file"""
    dataset_name = Leaf(str, set=set_dataset_name)
    """How often the dataset should be updated with new buffer data"""
    write_period = Leaf(int, set=set_write_period)
