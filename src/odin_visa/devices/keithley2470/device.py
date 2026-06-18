import asyncio
from odin_control.adapters.async_parameter_tree import AsyncParameterTree
import logging
from typing import final
from pyvisa.resources import MessageBasedResource
from ..device import Device
from ..device_config import DeviceType
from .state import K2470State
from .transport import K2470Transport
from .driver import K2470Driver
from .tree import K2470Tree


@final
class K2470Device(Device):
    def __init__(self, device: MessageBasedResource, ident: str):
        logging.info(f"Initialising `{ident}` as K2470Device")
        self.state = K2470State(
            kind=DeviceType.K2470, ident=ident, address=device._resource_name
        )
        self.transport = K2470Transport(device)
        self.driver = K2470Driver(self.transport)
        self.tree = K2470Tree(self.state, self.driver)

        logging.info("Setting default values on the K2470")

        logging.info(f"Initialised `{ident}`")

    async def set_default_values(self):
        await self.tree.set_from_state()

    def get_param_tree(self) -> AsyncParameterTree:
        return self.tree.tree

    async def refresh_param_tree(self):
        return await self.tree.refresh()

    async def update_task(self):
        i = 0
        while True:
            try:
                if i % 4 == 0:
                    logging.info("1 in 4 update")
                await self.refresh_param_tree()

                i += 1
                await asyncio.sleep(self.state.poll_freq)
            except asyncio.CancelledError:
                raise
