import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State

logger = structlog.get_logger()


class OutputTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state.config.output
        self.driver = driver
        self.tree = AsyncParameterTree(
            {
                "smode": (
                    lambda: str(self.state.smode),
                    self.driver.output.set_smode,
                ),
                "interlock": (
                    lambda: self.state.interlock,
                    self.driver.output.set_interlock,
                ),
                "interlock_tripped": (lambda: self.state.interlock_tripped, None),
                "enabled": (
                    lambda: self.state.enabled,
                    self.driver.output.set_enabled,
                ),
                "terminals": (
                    lambda: str(self.state.terminals),
                    self.driver.output.set_terminals,
                ),
            }
        )

    async def set_from_state(self) -> None:
        await self.driver.output.set_smode(self.state.smode)
        await self.driver.output.set_interlock(self.state.interlock)
        await self.driver.output.set_enabled(self.state.enabled)
        await self.driver.output.set_terminals(self.state.terminals)

    async def refresh(self) -> None:
        function = await self.driver.output.get_function()

        (
            self.state.smode,
            self.state.interlock,
            self.state.interlock_tripped,
            self.state.enabled,
            self.state.terminals,
        ) = await self.driver.execute(
            [
                self.driver.output.get_smode(function),
                self.driver.output.get_interlock(),
                self.driver.output.get_interlock_tripped(),
                self.driver.output.get_enabled(),
                self.driver.output.get_terminals(),
            ]
        )
