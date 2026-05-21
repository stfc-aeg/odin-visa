import logging
from pathlib import Path
from typing import cast
import numpy as np
import h5py
from odin_visa.devices.keithley2470.config import SaveFileConfig
from odin_visa.devices.keithley2470.managers import (
    BufferManager,
)
from odin_visa.devices.keithley2470.managers.buffer_manager import ITEM_DTYPE


class SaveFileManager:
    # TODO: more save options (multi-file, compression, etc..)

    def __init__(self, buffer_manager: BufferManager, config: SaveFileConfig):
        self.current_file = None
        self.current_dataset = None

        self.buffer_manager = buffer_manager
        self.config = config

        self.is_acquiring = False
        self.since_last_write = 0

    def start_acquisition(self):
        # TODO: figure out how to handle files/datasets
        #        - what to do if the file already exists?
        #        - what to do if the dataset already exists?
        #        - how do other adapters handle acquisitions? file per acquisitions? dataset per? multiple-file per acquisitions (for long acquisitions?)
        #        - how should all this be exposed?
        path = Path(self.config.filepath).joinpath(Path(self.config.filename))
        self.current_file = h5py.File(path, "a")
        logging.debug(f"created file: {self.current_file}")
        self.current_dataset = self.current_file.create_dataset(
            self.config.dataset_name, (0,), maxshape=(None,), dtype=ITEM_DTYPE
        )
        logging.debug(f"created dataset: {self.current_dataset}")
        self.since_last_write = 0
        self.is_acquiring = True

    def stop_acquisition(self):
        self.write()
        self.is_acquiring = False

    def update(self):
        logging.debug(f"savefile: update (since_last_write: {self.since_last_write})")
        if self.is_acquiring:
            self.since_last_write += 1
            if self.since_last_write == self.config.write_period:
                self.write()
                self.since_last_write = 0

    def write(self):
        logging.debug(f"savefile: write!")
        if self.current_dataset:
            size = len(self.current_dataset)
            logging.debug(f"current dataset size: {size}")
            new_items = self.buffer_manager.get_buffer(start=size)
            logging.debug(f"new items size: {size}")
            self.current_dataset.resize((size + len(new_items),))
            self.current_dataset[size:] = new_items
        else:
            logging.warning(
                "Attempted to write to h5 dataset, but no dataset has been set"
            )
