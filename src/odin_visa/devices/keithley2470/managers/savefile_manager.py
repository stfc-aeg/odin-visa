import logging
from pathlib import Path
from typing import TYPE_CHECKING, cast
import numpy as np
import h5py
from numpy.typing import NDArray
from odin_visa.devices.keithley2470.config import SaveFileConfig
from odin_visa.devices.keithley2470.managers import ITEM_DTYPE

if TYPE_CHECKING:
    from odin_visa.devices.keithley2470.k2470 import K2470Device


class SaveFileManager:
    # TODO: more save options (multi-file, compression, etc..)

    def __init__(self, device: "K2470Device"):
        self.path = Path()
        self.file = None
        self.dataset_name = ""
        self.config = device.control.config.savefile

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
        self.file = h5py.File(self.path, "a")
        self.file.create_dataset(
            self.dataset_name,
            shape=(0,),
            maxshape=(None,),
            dtype=ITEM_DTYPE,
            compression="gzip",
        )

    def save_chunk(self, chunk: NDArray):
        if self.file is None:
            logging.warning("attempted to save chunk while no file is opened")
            return

        ds = self.file[self.dataset_name]
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
        if self.file is None:
            logging.warning("attempted to read data while no file is opened")
            return

        ds = self.file[self.dataset_name]
        if not isinstance(ds, h5py.Dataset):
            logging.error(
                "Could not access dataset %s in %s",
                self.dataset_name,
                self.path,
            )
            return

        return ds[:]
