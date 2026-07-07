import h5py
import hdf5plugin
import structlog
from numpy.typing import NDArray

from odin_visa.devices.keithley2470.driver.types import ITEM_DTYPE
from odin_visa.devices.keithley2470.state import K2470State

logger = structlog.get_logger()


class FileWriter:
    def __init__(self, state: K2470State) -> None:
        self.state = state.config.savefile

    def create_file(self) -> None:
        if self.state.path().is_file():
            logger.warning("File already exists", path=self.state.path())
            return

        with h5py.File(self.state.path(), "w") as f:
            f.create_dataset(
                "measurements",
                shape=(0,),
                maxshape=(None,),
                dtype=ITEM_DTYPE,
                # TODO: benchmark different compression algorithms
                compression=hdf5plugin.Blosc(shuffle=hdf5plugin.Blosc.NOSHUFFLE),
            )
        # TODO: write metadata

    def write_chunk(self, chunk: NDArray) -> None:
        with h5py.File(self.state.path(), "a") as f:
            ds = f["measurements"]
            if not isinstance(ds, h5py.Dataset):
                logger.error(
                    "Could not access measurements dataset", path=self.state.path
                )
                return

            old_len = ds.shape[0]
            ds.resize(old_len + len(chunk), axis=0)
            ds[old_len:] = chunk

    def read(self) -> None:
        with h5py.File(self.state.path(), "r") as f:
            ds = f["measurements"]
            if not isinstance(ds, h5py.Dataset):
                logger.error(
                    "Could not access 'measurements' dataset", path=self.state.path()
                )
                return
