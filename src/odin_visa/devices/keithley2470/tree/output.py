import structlog
from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.driver import K2470Driver
from odin_visa.devices.keithley2470.state import K2470State

logger = structlog.get_logger()


class OutputTree:
    def __init__(self, state: K2470State, driver: K2470Driver) -> None:
        self.state = state.config.output
        self.driver = driver.output
        self.tree = AsyncParameterTree(
            {
                "smode": (lambda: str(self.state.smode), self.driver.set_smode),
                "interlock": (lambda: self.state.interlock, self.driver.set_interlock),
                "interlock_tripped": (lambda: self.state.interlock_tripped, None),
                "enabled": (lambda: self.state.enabled, self.driver.set_enabled),
                "terminals": (
                    lambda: str(self.state.terminals),
                    self.driver.set_terminals,
                ),
            }
        )

    async def set_from_state(self) -> None:
        await self.driver.set_smode(self.state.smode)
        await self.driver.set_interlock(self.state.interlock)
        await self.driver.set_enabled(self.state.enabled)
        await self.driver.set_terminals(self.state.terminals)

    async def refresh(self) -> None:
        self.state.smode = await self.driver.get_smode()
        self.state.interlock = await self.driver.get_interlock()
        self.state.interlock_tripped = await self.driver.get_interlock_tripped()
        self.state.enabled = await self.driver.get_enabled()
        self.state.terminals = await self.driver.get_terminals()
