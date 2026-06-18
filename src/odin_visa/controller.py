from __future__ import annotations
import asyncio
from odin_control.adapters.async_parameter_tree import AsyncParameterTree
from odin_control.adapters.async_base_controller import AsyncBaseController

from concurrent.futures.thread import ThreadPoolExecutor
import threading
import logging
from typing import Any
import pyvisa

from pyvisa.resources import MessageBasedResource

from odin_control.adapters.parameter_tree import ParameterTreeError

from odin_visa.devices.device import Device
from odin_visa.devices.device_config import DeviceType, DevicesConfig
from odin_visa.devices.keithley2470.device import K2470Device
from odin_visa.devices.keithley2470.driver.error import DriverError

# Suppress pyvisa's verbose debug logging during resource enumeration
logging.getLogger("pyvisa").setLevel(logging.ERROR)
logging.getLogger("gpib").setLevel(logging.ERROR)


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

    def __init__(self, options: dict[str, str]):
        logging.info("Initialising odin_visa")

        self.options = options
        self._background_tasks = set()

        logging.debug("Reading devices config")
        devices_config_path = self.options["devices_config"]
        with open(devices_config_path, "r") as f:
            devices_config = DevicesConfig.from_json(f.read())
            if isinstance(devices_config, list):
                logging.error("Invalid JSON config")
                return
            self.devices_config = devices_config
        logging.debug(
            f"Read config. Expecting {len(self.devices_config.devices)} devices"
        )

        self.visa_timeout_ms = int(self.options.get("visa_timeout_ms", 2000))

        # Ensure a single SCPI command is sent at a time across all devices
        self.lock: threading.Lock = threading.Lock()

        self.devices: dict[str, Device] = {}

        self.poll_interval = 1.0
        self.resource_manager = pyvisa.ResourceManager()

        self._initialise = self.initialise_devices()

        logging.info("odin_visa initialised")

    async def initialise_devices(self):
        logging.info("Discovering and initialising devices")
        configured = 0
        for device in self.devices_config.devices:
            logging.info(f"Attempting connection to `{device.address}`")
            address = device.address
            try:
                logging.debug(f"Opening {address}")
                resource = self.resource_manager.open_resource(
                    address, open_timeout=self.visa_timeout_ms
                )
            except Exception as e:
                logging.warning(f"Could not open device: `{address}` ({e})")
                continue

            # pyvisa also supports RegisterBasedResources - but these are controlled differently
            if not isinstance(resource, MessageBasedResource):
                logging.warning(
                    f"{address} is not a MessageBasedResource, and is therefore unsupported"
                )
                continue
            resource.timeout = self.visa_timeout_ms

            try:
                logging.debug(f"Trying to indentify {address}")
                ident = resource.query("*IDN?").strip()
                logging.debug(f"{address} identified as {ident}")
            except Exception as e:
                logging.warning(f"Could not query device: {address} ({e})")
                continue

            logging.info(f"Connected to device, identified as `{ident}`")

            try:
                match device.type:
                    case DeviceType.K2470:
                        device_obj = K2470Device(resource, ident)
                        await device_obj.set_default_values()
                        self.devices[device.name] = device_obj

                        configured += 1
            except DriverError as e:
                logging.error(f"Could not set default values for `{ident}`:\n{e}")

        logging.info(f"{configured} devices initialised")

        self.param_tree = await AsyncParameterTree(
            {
                "num_devices": (lambda: len(self.devices), None),
                "devices": {
                    name: device.get_param_tree()
                    for name, device in self.devices.items()
                },
            }
        )

    async def initialize(self, adapters):
        await super().initialize(adapters)

        for _, device in self.devices.items():
            self._start_background_task(device.update_task())

    def _start_background_task(self, coroutine):
        task = asyncio.create_task(coroutine)
        self._background_tasks.add(task)
        task.add_done_callback(self._background_tasks.discard)
        return task

    async def get(self, path, with_metadata=False) -> Any:
        try:
            return await self.param_tree.get(path, with_metadata)
        except ParameterTreeError as e:
            raise ParameterTreeError(e)

    async def set(self, path, data):
        try:
            await self.param_tree.set(path, data)
        except ParameterTreeError as e:
            raise ParameterTreeError(e)
        except DriverError as e:
            logging.error(f"Failed to set `{data}` at `{path}`:\n{e}")
            return

        # TODO: Ideally, this should only refresh the device that was 'set'
        for name, device in self.devices.items():
            try:
                await device.refresh_param_tree()
            except DriverError as e:
                logging.error(
                    f"Failed to refresh parameter tree for `{name}` after setting `{path}`:\n{e}"
                )

    async def cleanup(self):
        for task in self._background_tasks:
            task.cancel()

        await asyncio.gather(
            *self._background_tasks,
            return_exceptions=True,
        )

        self._background_tasks.clear()

    # def cleanup(self):
    #     # self.stop_background_task()
    #     # for name, device in self.devices.items():
    #     #     try:
    #     #         device.cleanup()
    #     #     except Exception:
    #     #         logging.exception("Error cleaning up device %s", name)
    #     self.executor.shutdown(wait=False, cancel_futures=True)
    #     try:
    #         self.resource_manager.close()
    #     except Exception:
    #         logging.exception("Error closing VISA resource manager")
    #
    # def initialize(self, adapters):
    #     pass

    # def start_background_task(self):
    #     self._stop_event.clear()
    #     self._background_future = self.background_task()
    #
    # def stop_background_task(self):
    #     self._stop_event.set()

    # @run_on_executor
    # def background_task(self):
    #     logging.info("Background task running")
    #     while not self._stop_event.wait(self.poll_interval):
    #         for name, device in self.devices.items():
    #             if self._stop_event.is_set():
    #                 break
    #             try:
    #                 device.update()
    #             except Exception:
    #                 logging.exception("Error updating device %s", name)
    #     logging.info("Background task stopped")
