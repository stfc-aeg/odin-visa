from __future__ import annotations
from gpib_ctypes.gpib.gpib import dev

from concurrent.futures.thread import ThreadPoolExecutor
import json
import threading
import logging
from typing import Any
import pyvisa

from pyvisa.resources import MessageBasedResource
from tornado.concurrent import run_on_executor

from odin_control.adapters.parameter_tree import ParameterTree, ParameterTreeError
from odin_control.adapters.base_controller import BaseController

from odin_visa.devices.device import Device
from odin_visa.devices.device_config import DeviceType, DevicesConfig
from odin_visa.devices.keithley2470.k2470 import K2470Device
from odin_visa.tree import ParameterTreeMixin

# Suppress pyvisa's verbose debug logging during resource enumeration
logging.getLogger("pyvisa").setLevel(logging.ERROR)
logging.getLogger("gpib").setLevel(logging.ERROR)


class VisaController(BaseController):
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
        self.options = options
        self.executor = ThreadPoolExecutor(max_workers=1)
        self._stop_event = threading.Event()
        self._background_future = None

        devices_config_path = self.options["devices_config"]
        with open(devices_config_path, "r") as f:
            devices_config = DevicesConfig.from_json(f.read())
            if isinstance(devices_config, list):
                logging.error("Invalid JSON config")
                return
            self.devices_config = devices_config

        self.visa_timeout_ms = int(self.options.get("visa_timeout_ms", 2000))

        # Ensure a single SCPI command is sent at a time across all devices
        self.lock: threading.Lock = threading.Lock()

        self.devices: dict[str, Device] = {}

        self.poll_interval = 1.0
        self.resource_manager = pyvisa.ResourceManager()

        self.param_tree: ParameterTree = self.initialise_devices()

        self.start_background_task()

    def initialise_devices(self):
        """Discovers and initializes VISA devices matching the given query.

        Uses pyvisa to list available resources, opens each one, queries *IDN?,
        and creates a device instance for any recognized instrument.

        Only MessageBasedResource devices are supported (GPIB, USB-TMC, TCPIP).
        RegisterBasedResources are logged and skipped.

        Args:
            devices_query: A pyvisa resource filter string (e.g., 'GPIB*::INSTR').
                If None or empty, no devices are returned.

        Returns:
            A ParameterTree containing the device count and all device subtrees.
        """
        for device in self.devices_config.devices:
            address = device.address
            try:
                logging.debug(f"Opening {address}")
                resource = self.resource_manager.open_resource(
                    address, open_timeout=self.visa_timeout_ms
                )
            except Exception as e:
                logging.warning(f"Could not open device: {address} ({e})")
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
                ident = resource.query("*IDN?")
                logging.debug(f"{address} identified as {ident}")
            except Exception as e:
                logging.warning(f"Could not query device: {address} ({e})")
                continue

            if device.type == DeviceType.K2470:
                self.devices[device.name] = K2470Device(
                    resource, ident, self.lock, device
                )

        return ParameterTree(
            {
                "poll_interval": (lambda: self.poll_interval, self.set_poll_interval),
                "num_devices": (lambda: len(self.devices), None),
                "devices": {
                    name: device.as_tree() for name, device in self.devices.items()
                },
            }
        )

    def set_poll_interval(self, value: float):
        self.poll_interval = value

    def get(self, path, with_metadata=False) -> Any:
        return self.param_tree.get(path, with_metadata)

    def set(self, path, data):
        try:
            self.param_tree.set(path, data)
        except ParameterTreeError as e:
            raise ParameterTreeError(e)

    def cleanup(self):
        self.stop_background_task()
        for name, device in self.devices.items():
            try:
                device.cleanup()
            except Exception:
                logging.exception("Error cleaning up device %s", name)
        self.executor.shutdown(wait=False, cancel_futures=True)
        try:
            self.resource_manager.close()
        except Exception:
            logging.exception("Error closing VISA resource manager")

    def initialize(self, adapters):
        pass

    def start_background_task(self):
        self._stop_event.clear()
        self._background_future = self.background_task()

    def stop_background_task(self):
        self._stop_event.set()

    @run_on_executor
    def background_task(self):
        logging.info("Background task running")
        while not self._stop_event.wait(self.poll_interval):
            for name, device in self.devices.items():
                if self._stop_event.is_set():
                    break
                try:
                    device.update()
                except Exception:
                    logging.exception("Error updating device %s", name)
        logging.info("Background task stopped")
