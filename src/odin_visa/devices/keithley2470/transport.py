from pyvisa import VisaIOError
import asyncio
from timeit import default_timer
import logging
from pyvisa.resources import MessageBasedResource


class TransportError(Exception):
    pass


class K2470Transport:
    def __init__(self, device: MessageBasedResource):
        self.device = device
        self._lock = asyncio.Lock()

    async def write(self, cmd: str) -> None:
        async with self._lock:
            start = default_timer()

            # TODO: Device error handling?
            try:
                await asyncio.to_thread(self.device.write, cmd)
            except VisaIOError as e:
                raise TransportError(
                    f"Failed to write `{cmd}` to `{self.device._resource_name}`"
                ) from e

            end = default_timer()
            logging.debug("write(`%s`) took %fus", cmd, (end - start) * 1_000_000)

    async def query(self, cmd: str) -> str:
        async with self._lock:
            start = default_timer()

            # TODO: Device error handling?
            try:
                msg = await asyncio.to_thread(self.device.query, cmd)
            except VisaIOError as e:
                raise TransportError(
                    f"Failed to send query `{cmd}` to `{self.device._resource_name}`"
                ) from e

            msg = msg.strip()

            end = default_timer()
            logging.debug(
                "query(`%s`) took %fus, returning `%s`",
                cmd,
                (end - start) * 1_000_000,
                msg,
            )
            return msg
