import numpy as np
import pandas as pd
import structlog

from odin_visa.devices.keithley2470.driver.error import (
    InvalidBufferSizeError,
    InvalidResponseError,
)
from odin_visa.devices.keithley2470.driver.types import (
    MeasurementNDArray,
)
from odin_visa.devices.keithley2470.transport import K2470Transport
from odin_visa.util.instrument import instrument
from odin_visa.util.scpi_parse import parse_int

logger = structlog.get_logger()


class BufferDriver:
    def __init__(self, transport: K2470Transport) -> None:
        self.transport = transport

    @instrument(logger)
    async def create_buffer(self, name: str, size: int) -> None:
        await self.transport.write(
            f':TRAC:MAKE "{name}", {size} ;'
            f':TRAC:FILL:MODE CONT, "{name}"'
        )  # fmt: skip

    @instrument(logger)
    async def delete_buffer(self, name: str) -> None:
        await self.transport.write(f':TRAC:DEL "{name}"')

    @instrument(logger)
    async def get_buffer_size(self, name: str) -> int:
        response = await self.transport.query(f':TRAC:POIN? "{name}"')
        try:
            return parse_int(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    @instrument(logger)
    async def get_last_measurement_index(self, name: str) -> int:
        response = await self.transport.query(f':TRAC:ACT:END? "{name}"')
        try:
            return parse_int(response)
        except ValueError as e:
            raise InvalidResponseError(response) from e

    async def read_measurements(
        self, name: str, start_index: int
    ) -> tuple[MeasurementNDArray, int] | None:
        size = await self.get_buffer_size(name)
        last_element_idx = await self.get_last_measurement_index(name)
        if last_element_idx == 0:
            logger.debug("buffer is empty")
            return None

        if start_index == (last_element_idx + 1) % size:
            logger.debug("no new buffer elements")
            return None
        if start_index < (last_element_idx + 1) % size:
            logger.debug(
                "regular buffer read",
                start_index=start_index,
                end_index=last_element_idx,
            )
            measurements = await self._read_measurements(
                name, start_index, last_element_idx
            )
            if measurements is None:
                return None
            return (
                measurements,
                (last_element_idx + 1) % size,
            )

        logger.debug(
            "wrapping buffer read",
            start_index=start_index,
            end_index=last_element_idx,
        )
        to_buf_end = await self._read_measurements(name, start_index, size)
        from_buf_start = await self._read_measurements(name, 1, last_element_idx)
        if from_buf_start is None or to_buf_end is None:
            return None

        return (pd.concat([to_buf_end, from_buf_start]), (last_element_idx + 1) % size)

    async def _read_measurements(
        self, name: str, start: int, end: int
    ) -> MeasurementNDArray | None:
        data_points = ((end - start) + 1) * 3
        items = np.asarray(
            await self.transport.query_bytes(
                f':TRAC:DATA? {start}, {end}, "{name}", REL, SOUR, READ', data_points
            ),
            dtype=np.float64,
        )
        items[::3] *= 1_000_000
        rows = items.reshape(-1, 3)
        return pd.DataFrame(
            {
                "reading": rows[:, 1],
                "source": rows[:, 2],
            },
            index=pd.to_timedelta(rows[:, 0], unit="us"),
        ).rename_axis("timestamp")

    async def _read_measurements_str(
        self, name: str, start: int, end: int
    ) -> MeasurementNDArray | None:
        return self._parse_response_str(
            await self.transport.query(
                f':TRAC:DATA? {start}, {end}, "{name}", REL, SOUR, READ'
            )
        )

    def _parse_response_str(self, response: str) -> MeasurementNDArray | None:
        items = np.fromstring(response, sep=",")

        if items.size == 0:
            return None
        if items.size % 3 != 0:
            raise InvalidBufferSizeError(items.size)

        items[::3] *= 1_000_000
        rows = items.reshape(-1, 3)
        return pd.DataFrame(
            {
                "reading": rows[:, 1],
                "source": rows[:, 2],
            },
            index=pd.to_timedelta(rows[:, 0], unit="us"),
        ).rename_axis("timestamp")
