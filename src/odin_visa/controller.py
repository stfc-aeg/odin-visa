from __future__ import annotations

import asyncio
import logging
import threading
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pyvisa
import structlog
from odin_control.adapters.async_base_controller import AsyncBaseController
from odin_control.adapters.async_parameter_tree import AsyncParameterTree
from pyvisa import VisaIOError
from pyvisa.resources import MessageBasedResource
from structlog.dev import ConsoleRenderer
from typing_extensions import override

from odin_visa.devices.device import Device, DeviceError
from odin_visa.devices.device_config import DevicesConfig, DeviceType
from odin_visa.devices.keithley2470.device import K2470Device

if TYPE_CHECKING:
    from asyncio.tasks import Task
    from collections.abc import Coroutine

# Suppress pyvisa's verbose debug logging during resource enumeration
logging.getLogger("pyvisa").setLevel(logging.ERROR)
logging.getLogger("gpib").setLevel(logging.ERROR)

structlog.stdlib.recreate_defaults()
renderer = ConsoleRenderer.get_active()
renderer.level_styles = {
    **renderer.level_styles,
    "debug": "\x1b[90m",  # bright black / commonly gray
}

logger = structlog.get_logger()


class VisaController(AsyncBaseController):
    """ODIN controller that manages VISA instrument discovery and communication.

    Discovers connected instruments via pyvisa, identifies them by *IDN?,
    and creates device-specific instances for known models. Exposes all
    devices through a unified ODIN ParameterTree.

    Runs a background polling thread that calls update() on each device
    every second to refresh live instrument state.

    All SCPI commands across all devices are serialized through a shared
    threading.Lock to prevent interleaved VISA communication.
    """

    def __init__(self, options: dict[str, str]) -> None:
        logger.info("Initialising odin_visa")

        self.options = options
        self._background_tasks = set()

        logger.debug("Reading devices config")
        devices_config_path = self.options["devices_config"]
        with Path(devices_config_path).open("r") as f:
            devices_config = DevicesConfig.from_json(f.read())
            if isinstance(devices_config, list):
                logger.error("Invalid JSON config")
                return
            self.devices_config = devices_config
        logger.debug("read config", device_count=len(self.devices_config.devices))

        self.visa_timeout_ms = int(self.options.get("visa_timeout_ms", 2000))

        # Ensure a single SCPI command is sent at a time across all devices
        self.lock: threading.Lock = threading.Lock()

        self.devices: dict[str, Device] = {}

        self.poll_interval = 1.0
        self.resource_manager = pyvisa.ResourceManager()

        self._initialise = self.initialise_devices()

        logger.info("odin_visa initialised")

    @override
    async def initialize(self, adapters: dict[str, object]) -> None:
        await super().initialize(adapters)

        for device in self.devices.values():
            self._start_background_task(device.update_task())

    @override
    async def get(self, path: str, with_metadata: bool = False) -> Any:
        return await self.param_tree.get(path, with_metadata)

    @override
    async def set(self, path: str, data: Any) -> None:
        try:
            await self.param_tree.set(path, data)
        except DeviceError:
            logger.exception("Failed to set parameter", path=path, data=data)
            return

        # TODO: Ideally, this should only refresh the device that was 'set'
        log_name = ""
        try:
            for name, device in self.devices.items():
                log_name = name
                await device.refresh_param_tree()
        except DeviceError:
            logger.exception(
                "Failed to refresh parameter tree",
                device=log_name,
                path=path,
            )

    @override
    async def cleanup(self) -> None:
        for task in self._background_tasks:
            task.cancel()

        await asyncio.gather(
            *self._background_tasks,
            return_exceptions=True,
        )

        self._background_tasks.clear()

    async def initialise_devices(self) -> None:
        logger.info("Discovering and initialising devices")
        configured = 0
        for device in self.devices_config.devices:
            logger.info("Attempting connection to `%s`", device.address)
            address = device.address
            try:
                logger.debug("Opening %s", address)
                resource = self.resource_manager.open_resource(
                    address, open_timeout=self.visa_timeout_ms
                )
            except (ValueError, VisaIOError) as e:
                logger.warning("Could not open device: `%s` (%s)", address, e)
                continue

            # pyvisa also supports RegisterBasedResources - but these are controlled differently
            if not isinstance(resource, MessageBasedResource):
                logger.warning(
                    "%s is not a MessageBasedResource, and is therefore unsupported",
                    address,
                )
                continue

            resource.timeout = self.visa_timeout_ms

            logger.debug("Trying to indentify %s", address)
            try:
                ident = resource.query("*IDN?").strip()
            except VisaIOError:
                logger.exception("Could not query device `%s`", address)
                continue

            logger.info("Connected to device, identified as `%s`", ident)

            match device.type:
                case DeviceType.K2470:
                    try:
                        device_obj = K2470Device(resource, ident, address)
                        await device_obj.set_default_values()
                    except DeviceError:
                        logger.exception("Could not initialize `%s`", ident)
                        continue
                    logger.info("Initialised %s (%s)", ident, address)
                    self.devices[device.name] = device_obj
                    configured += 1

        logger.info("%i devices initialised", configured)

        self.param_tree = await AsyncParameterTree(
            {
                "num_devices": (lambda: len(self.devices), None),
                "devices": {
                    name: device.get_param_tree()
                    for name, device in self.devices.items()
                },
            }
        )

    def _start_background_task(self, coroutine: Coroutine) -> Task:
        task = asyncio.create_task(coroutine)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)
        return task
