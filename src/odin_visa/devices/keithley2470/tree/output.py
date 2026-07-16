import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State
from odin_visa.devices.keithley2470.transport import DeviceMiscError

logger = structlog.get_logger()


class OutputTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state
        self.driver = driver
        self.tree = AsyncParameterTree(
            {
                "smode": (
                    lambda: str(self.state.config.output.smode),
                    self.driver.output.set_smode,
                ),
                "interlock": (
                    lambda: self.state.config.output.interlock,
                    self.driver.output.set_interlock,
                ),
                "interlock_tripped": (
                    lambda: self.state.config.output.interlock_tripped,
                    None,
                ),
                "enabled": (
                    lambda: self.state.config.output.enabled,
                    self.driver.output.set_enabled,
                ),
                "terminals": (
                    lambda: str(self.state.config.output.terminals),
                    self.driver.output.set_terminals,
                ),
            }
        )

    async def set_from_state(self) -> None:
        await self.driver.output.set_smode(self.state.config.output.smode)
        await self.driver.output.set_interlock(self.state.config.output.interlock)
        await self.driver.output.set_enabled(self.state.config.output.enabled)
        await self.driver.output.set_terminals(self.state.config.output.terminals)

    async def refresh(self) -> None:
        function = await self.driver.output.get_function()

        try:
            (
                self.state.config.output.smode,
                self.state.config.output.interlock,
                self.state.config.output.interlock_tripped,
                self.state.config.output.enabled,
                self.state.config.output.terminals,
            ) = await self.driver.execute(
                [
                    self.driver.output.get_smode(function),
                    self.driver.output.get_interlock(),
                    self.driver.output.get_interlock_tripped(),
                    self.driver.output.get_enabled(),
                    self.driver.output.get_terminals(),
                ]
            )
        except DeviceMiscError as e:
            logger.error("Device returned errors, appending to event log.", errors=e)
            for error in e.messages:
                self.state.event_log.append(error)
