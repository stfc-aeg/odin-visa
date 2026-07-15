from odin_control.adapters.async_parameter_tree import AsyncParameterTree

from odin_visa.devices.keithley2470.state import K2470State


class EventLogTree:
    def __init__(
        self,
        state: K2470State,
    ) -> None:
        self.state = state.event_log

        self.tree = AsyncParameterTree(
            {
                "count": (lambda: self.state.count, None),
                "last_event": (self._get_last_event, None),
                "events": (self._get_events, None),
            }
        )

    def _get_last_event(self) -> dict:
        event = self.state.last_event
        if event is None:
            return {}
        return event.to_dict()

    def _get_events(self) -> list[dict]:
        return [event.to_dict() for event in self.state.log]
