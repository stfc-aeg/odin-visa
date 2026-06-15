from numpy.typing import NDArray
import hdf5plugin
from odin_visa.types import Result, Ok, Err
import os
import h5py
from odin_visa.tree import ParameterTreeMixin
from odin_visa.devices.keithley2470.managers import ITEM_DTYPE
from odin_visa.devices.keithley2470.config.savefile import SaveFileConfigTree


class FileWriter(ParameterTreeMixin):
    def __init__(self, config_tree: SaveFileConfigTree):
        self.path = config_tree.path

    def create_file(self) -> Result[None, str]:
        if os.path.isfile(self.path):
            return Err(f"`{self.path}` already exists")

        try:
            with h5py.File(self.path, "w") as f:
                f.create_dataset(
                    "measurements",
                    shape=(0,),
                    maxshape=(None,),
                    dtype=ITEM_DTYPE,
                    # TODO: benchmark different compression algorithms
                    compression=hdf5plugin.Blosc2(filters=hdf5plugin.Blosc2.NOFILTER),
                )
        except Exception as e:
            return Err(str(e))

        # TODO: write metadata

        return Ok(None)

    def write_chunk(self, chunk: NDArray) -> Result[None, str]:
        with h5py.File(self.path, "a") as f:
            ds = f["measurements"]
            if not isinstance(ds, h5py.Dataset):
                return Err(f"Could not access 'measurements' dataset in {self.path}")

            try:
                old_len = ds.shape[0]
                ds.resize(old_len + len(chunk), axis=0)
                ds[old_len:] = chunk
            except Exception as e:
                return Err(str(e))

        return Ok(None)

    def read(self) -> Result[NDArray, str]:
        try:
            with h5py.File(self.path, "r") as f:
                ds = f["measurements"]
                if not isinstance(ds, h5py.Dataset):
                    return Err(
                        f"Could not access 'measurements' dataset in {self.path}"
                    )
                return Ok(ds[:])
        except Exception as e:
            return Err(str(e))
