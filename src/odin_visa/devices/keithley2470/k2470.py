import logging
from threading import Lock
from timeit import default_timer
from typing import List, Optional

from pyvisa.resources import MessageBasedResource

from odin_visa.devices.device import Device
from odin_visa.devices.device_config import DeviceConfig, DeviceType
from odin_visa.devices.keithley2470.acquisitions.acquisitions import Acquisitions
from odin_visa.devices.keithley2470.acquisitions.buffers import Buffers
from odin_visa.devices.keithley2470.acquisitions.status import TriggerModelState
from odin_visa.devices.keithley2470.config import Config
from odin_visa.devices.keithley2470.event_log import EventLog
from odin_visa.devices.keithley2470.managers.buffer_manager import BufferManager
from odin_visa.tree import Leaf, ParameterTreeMixin, SubTree


class Control(ParameterTreeMixin):
    def __init__(
        self,
        device: "K2470Device",
        ident: str,
        address: str,
    ):
        self.event_log = EventLog()
        self.ident = ident
        self.address = address
        self.type = DeviceType.K2470
        self.config = Config(device)
        self.acquisitions = Acquisitions(device, self.config)

    event_log = SubTree(EventLog)
    ident = Leaf(str)
    address = Leaf(str)
    type = Leaf(DeviceType)
    acquisitions = SubTree(Acquisitions)
    config = SubTree(Config)


class K2470Device(Device):
    def __init__(
        self,
        resource: MessageBasedResource,
        ident: str,
        lock: Lock,
        config: DeviceConfig,
    ):
        self.device_control_enable: bool = True
        self.lock: Lock = lock
        self._device = resource
        self._config = config

        self.write("*RST")

        self.control = Control(self, ident, resource._resource_name)
        self._buffer_manager = BufferManager(self, self.control.config.buffer)
        self.buffers = Buffers(self, self._buffer_manager)

    def update(self):
        match self.control.acquisitions.status.state:
            case TriggerModelState.RUNNING | TriggerModelState.WAITING:
                running = True
            case _:
                running = False

        self.control.config.update(running)
        self.control.acquisitions.update()

    def cleanup(self):
        self.device_control_enable = False
        try:
            self.control.acquisitions.cleanup()
            self._buffer_manager.cleanup()
        except Exception:
            logging.exception(
                "Error cleaning up acquisitions for %s", self.control.address
            )
        try:
            self._device.close()
        except Exception:
            logging.exception("Error closing VISA resource %s", self.control.address)

    def query(
        self,
        cmd: str,
        suppress_error: Optional[List[int]] = None,
    ) -> str | None:
        if self.device_control_enable:
            with self.lock:
                try:
                    logging.debug("Query `%s`", cmd)
                    start = default_timer()

                    self._device.write(cmd)

                    # Check EAV (Error Available) bit — set when the error queue is non-empty.
                    # This prevents reading a stale or invalid response after a command error.
                    stb = self._device.read_stb()
                    if stb & 0x04:
                        self.check_error(suppress_error, cmd)
                        return None

                    ret = self._device.read().strip().strip('"')
                    self.check_error(suppress_error, cmd)

                    end = default_timer()
                    logging.debug(f"Response `{ret}` ({end - start:.3f} seconds)")
                    return ret
                except Exception as e:
                    if not self.device_control_enable:
                        logging.debug("Query `%s` failed during shutdown: %s", cmd, e)
                        return None
                    logging.error(
                        f"Error commincating to device: {e}. Querying error log"
                    )
                    self.check_error(suppress_error, cmd)
                    return None

    def write(
        self,
        cmd: str,
        suppress_error: Optional[List[int]] = None,
    ) -> None:
        if self.device_control_enable:
            with self.lock:
                try:
                    logging.debug(f"Write `{cmd}`")
                    start = default_timer()

                    self._device.write(cmd)
                    self.check_error(suppress_error, cmd)

                    end = default_timer()
                    logging.debug(f"Response ({end - start:.3f} seconds)")
                except Exception as e:
                    if not self.device_control_enable:
                        logging.debug("Write `%s` failed during shutdown: %s", cmd, e)
                        return
                    logging.error(
                        f"Error commincating to device: {e}. Querying error log"
                    )
                    self.check_error(suppress_error, cmd)

    def check_error(
        self, suppress_error: Optional[List[int]] = None, during_command: str = ""
    ):
        if not self.device_control_enable:
            return

        max_error_reads = 32
        for _ in range(max_error_reads):
            try:
                error_string = self._device.query(":SYST:ERR?").strip()
                error_code = int(error_string.split(",")[0])
                if suppress_error and error_code in suppress_error:
                    logging.debug("Suppressed device error: %s", error_string)
                    continue
            except Exception as e:
                logging.error(
                    f"Could not query the error log, is the device connected? ({e})"
                )
                error_string = f"Could not query error log: {e}"
                break

            if error_string != '0,"No error;0;0 0"':
                logging.error(f"Error log contains: {error_string}")
                self.control.event_log.push_event(error_string, during_command)
            else:
                break
        else:
            logging.error("Stopped reading error log after %d entries", max_error_reads)

        if not self.device_control_enable:
            return

        try:
            self._device.write("*CLS")
        except Exception as e:
            logging.error(f"Could not clear the error log ({e})")

    buffers = SubTree(Buffers)
    control = SubTree(Control)
