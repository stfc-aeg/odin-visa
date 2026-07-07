import pandas as pd
import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.device_config import DeviceConfig, ResampleMethod
from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.util.instrument import instrument

logger = structlog.get_logger()


class BufferTree:
    @instrument(logger, skip={"state"})
    def __init__(
        self, state: K2470State, driver: K2470Driver, config: DeviceConfig
    ) -> None:
        self.state = state.buffer
        self.driver = driver.buffer
        self.tree = AsyncParameterTree(
            {
                "range": (lambda: self.state.range, self._set_range),
                "buffer": (self._get_buffer, None),
            }
        )

    def _set_range(self, value: int) -> None:
        self.state.range = value

    @instrument(logger)
    def _get_buffer(self) -> list[tuple[float, float, float]]:
        if self.state.buffer is None:
            return []

        start = pd.to_timedelta(self.state.range, unit="s")
        df = self.state.buffer
        df = df.loc[df.index.max() - start :]
        # if bin_size is not None and resample_method is not None:
        #     df = df.ffill().resample(bin_size)
        # match resample_method:
        #     case ResampleMethod.Mean:
        #         df = df.mean()
        #     case ResampleMethod.Median:
        #         df = df.median()
        #     case ResampleMethod.Min:
        #         df = df.min()
        #     case ResampleMethod.Max:
        #         df = df.max()
        #     case ResampleMethod.First:
        #         df = df.first()

        return [
            (int(idx.value) / 1000, src, rdg)
            for idx, src, rdg in df.ffill().itertuples(index=True, name=None)
        ]
