import asyncio
from timeit import default_timer
from typing import final

import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree
from pyvisa.resources import MessageBasedResource
from typing_extensions import override

from odin_visa.devices.device import Device
from odin_visa.devices.device_config import DeviceConfig, DeviceType
from odin_visa.devices.keithley2470.managers.acquisition import Acquisition
from odin_visa.util.instrument import instrument, instrument_async

from .driver import K2470Driver
from .state import K2470State
from .transport import K2470Transport
from .tree import K2470Tree

logger = structlog.get_logger()


@final
class K2470Device(Device):
    def __init__(
        self,
        device: MessageBasedResource,
        config: DeviceConfig,
        ident: str,
        address: str,
    ) -> None:
        logger.info("Initialising K2470Device", ident=ident, address=address)
        self.config = config
        self.state = K2470State(kind=DeviceType.K2470, ident=ident, address=address)
        self.state.config.savefile.base_folder = self.config.savefile_config.data_folder
        self.transport = K2470Transport(device)
        self.driver = K2470Driver(self.transport)
        self.tree = K2470Tree(self.state, self.driver, self.config)

        self.acquisition = Acquisition(
            state=self.state, driver=self.driver, config=self.config
        )

    @instrument_async(logger)
    async def initialise(self) -> None:
        logger.info("Resetting K2470")
        await self.driver.reset()

        logger.info("Setting K2470 default values")
        await self.tree.set_from_state()

        logger.info("Creating device buffer")
        name = self.config.device_buffer.name
        size = self.config.device_buffer.size
        await self.driver.buffer.delete_buffer(name)
        await self.driver.buffer.create_buffer(name, size)

    @override
    @instrument(logger)
    def get_param_tree(self) -> AsyncParameterTree:
        return self.tree.tree

    @override
    @instrument_async(logger)
    async def refresh_param_tree(self) -> None:
        return await self.tree.refresh()

    @override
    async def update_task(self) -> None:
        i = 0
        while True:
            start = default_timer()
            await self.acquisition.update()
            await self.refresh_param_tree()

            i += 1
            end = default_timer()
            duration = end - start
            sleep_duration = self.state.poll_freq - duration
            logger.debug(
                "update finished, sleeping til next poll",
                sleep_duration=sleep_duration,
                update_duration=duration,
            )
            await asyncio.sleep(sleep_duration)

    @override
    async def cleanup(self) -> None:
        await self.acquisition.cleanup()
