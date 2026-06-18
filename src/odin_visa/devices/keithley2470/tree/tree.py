from odin_control.adapters.async_parameter_tree import AsyncParameterTree
from returns.result import Result
import logging
from ..state import K2470State
from ..driver import K2470Driver
from .config import ConfigTree


class K2470Tree:
    def __init__(self, state: K2470State, driver: K2470Driver):
        logging.debug("initialising K2470Tree")
        self.state = state
        self.driver = driver

        self.config_tree = ConfigTree(state, driver)

        self.tree = AsyncParameterTree(
            {
                "config": self.config_tree.tree,
                "ident": (lambda: self.state.ident, None),
                "address": (lambda: self.state.address, None),
                "type": (lambda: self.state.kind, None),
                "poll_freq": (
                    lambda: self.state.poll_freq,
                    lambda freq: setattr(self.state, "poll_freq", freq),
                ),
            }
        )
        logging.debug("initialised K2470Tree")

    async def set_from_state(self):
        return await self.config_tree.set_from_state()

    async def refresh(self):
        logging.debug("refreshing K2470Tree")
        await self.config_tree.refresh()
        logging.debug("refreshed K2470Tree")
