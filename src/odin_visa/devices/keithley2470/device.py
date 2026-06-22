import asyncio
from typing import final

import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree
from pyvisa.resources import MessageBasedResource

from odin_visa.devices.device import Device
from odin_visa.devices.device_config import DeviceType

from .driver import K2470Driver
from .state import K2470State
from .transport import K2470Transport
from .tree import K2470Tree

logger = structlog.get_logger()


@final
class K2470Device(Device):
    def __init__(self, device: MessageBasedResource, ident: str, address: str) -> None:
        logger.info("Initialising K2470Device", ident=ident, address=address)
        self.state = K2470State(kind=DeviceType.K2470, ident=ident, address=address)
        self.transport = K2470Transport(device)
        self.driver = K2470Driver(self.transport)
        self.tree = K2470Tree(self.state, self.driver)

    async def set_default_values(self) -> None:
        logger.info("Setting K2470 default values")
        await self.tree.set_from_state()

    def get_param_tree(self) -> AsyncParameterTree:
        return self.tree.tree

    async def refresh_param_tree(self) -> None:
        return await self.tree.refresh()

    async def update_task(self) -> None:
        i = 0
        while True:
            if i % 4 == 0:
                logger.info("1 in 4 update")
            await self.refresh_param_tree()

            i += 1
            await asyncio.sleep(self.state.poll_freq)
