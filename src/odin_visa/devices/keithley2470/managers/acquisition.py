import numpy as np
import pandas as pd
import structlog

from odin_visa.devices.keithley2470.device_config import K2470DeviceConfig
from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.driver.types import ITEM_DTYPE
from odin_visa.devices.keithley2470.managers.file_writer import FileWriter
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.devices.keithley2470.transport import DeviceMiscError

logger = structlog.get_logger()


class Acquisition:
    def __init__(
        self, state: K2470State, driver: K2470Driver, config: K2470DeviceConfig
    ) -> None:
        self.driver = driver
        self.state = state
        self.config = config

        self.file_writer = FileWriter(state, config)

        self.is_acquiring = False
        self.current_index = 1
        self.iteration = 0
        self.last_saved_index = 0

    async def update(self) -> None:
        if not self.is_acquiring:
            return

        self.iteration += 1

        res = await self.driver.buffer.read_measurements(
            self.config.device_buffer.name, self.current_index
        )
        if res is None:
            return
        new_measurements, new_index = res
        self.state.buffer.buffer = (
            pd.concat([self.state.buffer.buffer, new_measurements])
            if self.state.buffer.buffer is not None
            else new_measurements
        )
        logger.info(
            "Read buffer from device",
            new_measurements=len(new_measurements),
            total_measurements=len(self.state.buffer.buffer),
            avg_readings_per_iter=len(self.state.buffer.buffer) // self.iteration,
        )
        self.current_index = new_index

        if (
            self.state.config.savefile.enable
            and self.iteration % self.config.savefile_config.save_frequency == 0
        ):
            await self.save_chunk_to_disk()

    async def save_chunk_to_disk(self) -> None:
        logger.info("Saving chunk to disk")
        buffer = self.state.buffer.buffer
        if buffer is None:
            logger.warning("Buffer is none! Is an acqusition running?")
            return

        df = buffer.iloc[self.last_saved_index :]
        out = np.empty(len(df), dtype=ITEM_DTYPE)

        out["timestamp"] = df.index.asi8 // 1_000  # datetime ns -> microseconds
        out["reading"] = df["reading"].to_numpy()

        self.file_writer.write_chunk(out)
        self.last_saved_index = len(buffer) - 1

    async def start_acquisition(self) -> None:
        logger.info("Starting acqusition")
        if self.is_acquiring:
            logger.warning("Acquisition already running")
            return

        self.current_index = 1
        self.state.buffer.buffer = None
        self.file_writer.create_file()

        size = self.config.device_buffer.size
        name = self.config.device_buffer.name
        try:
            await self.driver.buffer.delete_buffer(name)
        except DeviceMiscError:
            logger.warning("Could not delete buffer, as it does not exist")
        await self.driver.buffer.create_buffer(name, size)

        await self.driver.trigger_model.load_loop_until_trigger_model(
            self.config.device_buffer.name
        )
        await self.driver.trigger_model.init()

        self.is_acquiring = True

    async def stop_acquisition(self) -> None:
        logger.info("Stopping acqusition")
        if not self.is_acquiring:
            logger.warning("No need to stop acqusition, one isn't running")
            return

        logger.debug("sending trigger")
        await self.driver.trigger_model.trigger()
        # TODO: wait for status change

        self.is_acquiring = False

    async def cleanup(self) -> None:
        if self.is_acquiring:
            await self.stop_acquisition()
