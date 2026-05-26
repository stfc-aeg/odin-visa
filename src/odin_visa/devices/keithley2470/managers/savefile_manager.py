import logging
from pathlib import Path
from typing import cast
import numpy as np
import h5py
from numpy.typing import NDArray
from odin_visa.devices.keithley2470.config import SaveFileConfig
from odin_visa.devices.keithley2470.managers import ITEM_DTYPE


class SaveFileManager:
    # TODO: more save options (multi-file, compression, etc..)

    def __init__(self, config: SaveFileConfig):
        self.path = Path()
        self.dataset_name = ""
        self.config = config

    def create_dataset(self):
        # TODO: figure out how to handle files/datasets
        #        - what to do if the file already exists?
        #        - what to do if the dataset already exists?
        #        - how do other adapters handle acquisitions? file per acquisitions? dataset per? multiple-file per acquisitions (for long acquisitions?)
        #        - how should all this be exposed?
        self.path = Path(self.config.filepath).joinpath(Path(self.config.filename))
        self.dataset_name = self.config.dataset_name
        logging.warning(
            "%s %s %s", self.config.filename, self.config.filepath, self.dataset_name
        )
        with h5py.File(self.path, "w") as f:
            f.create_dataset(
                self.dataset_name,
                shape=(0,),
                maxshape=(None,),
                dtype=ITEM_DTYPE,
                compression="gzip",
            )

    def save_chunk(self, chunk: NDArray):
        with h5py.File(self.path, "a") as f:
            ds = f[self.dataset_name]
            if not isinstance(ds, h5py.Dataset):
                logging.error(
                    "Could not access dataset %s in %s",
                    self.dataset_name,
                    self.path,
                )
                return
            old_len = ds.shape[0]
            ds.resize(old_len + len(chunk), axis=0)
            ds[old_len:] = chunk

    def read(self) -> NDArray | None:
        try:
            with h5py.File(self.path, "r") as f:
                ds = f[self.dataset_name]
                if not isinstance(ds, h5py.Dataset):
                    logging.error(
                        "Could not access dataset %s in %s",
                        self.dataset_name,
                        self.path,
                    )
                    return
                return ds[:]
        except:
            return
