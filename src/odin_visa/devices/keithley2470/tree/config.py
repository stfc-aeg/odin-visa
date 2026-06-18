from returns.result import Result
import logging
from odin_control.adapters.async_parameter_tree import AsyncParameterTree
from ..state import K2470State
from ..driver import K2470Driver
from .source import SourceTree


class ConfigTree:
    def __init__(self, state: K2470State, driver: K2470Driver):
        logging.debug("initialising Config")
        self.state = state
        self.driver = driver

        self.source_tree = SourceTree(state, driver)

        self.tree = AsyncParameterTree({"source": self.source_tree.tree})
        logging.debug("initialised ConfigTree")

    async def set_from_state(self):
        return await self.source_tree.set_from_state()

    async def refresh(self):
        logging.debug("refreshing ConfigTree")
        await self.source_tree.refresh()
        logging.debug("refreshed ConfigTree")
