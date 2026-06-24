import pandas as pd
import structlog

from odin_visa.devices.device_config import DeviceConfig
from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.util.instrument import instrument_async

logger = structlog.get_logger()


class Acquisition:
    def __init__(
        self, state: K2470State, driver: K2470Driver, config: DeviceConfig
    ) -> None:
        self.driver = driver
        self.state = state
        self.config = config

        self.is_acquiring = False
        self.current_index = 1
        self.iteration = 0

    @instrument_async(logger)
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
        self.state.buffers.buffer = (
            pd.concat([self.state.buffers.buffer, new_measurements])
            if self.state.buffers.buffer is not None
            else new_measurements
        )
        logger.info(
            "Read buffer from device",
            new_measurements=len(new_measurements),
            total_measurements=len(self.state.buffers.buffer),
            avg_readings_per_iter=len(self.state.buffers.buffer) // self.iteration,
        )
        self.current_index = new_index

    @instrument_async(logger)
    async def start_acquisition(self) -> None:
        logger.info("Starting acqusition")
        if self.is_acquiring:
            logger.warning("Acquisition already running")
            return

        self.state.buffers.buffer = None
        self.state.buffers.start_from = 0

        await self.driver.trigger_model.load_loop_until_trigger_model(
            self.config.device_buffer.name
        )
        await self.driver.trigger_model.init()

        self.is_acquiring = True

    @instrument_async(logger)
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
