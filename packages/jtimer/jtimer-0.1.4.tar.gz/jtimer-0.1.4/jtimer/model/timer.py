from datetime import timedelta
from jtimer.model.time_event import TimeEvent, TimeEventType


class Timer:
    def __init__(
        self, id: int, name: str, events: list = [], delta: timedelta = timedelta()
    ) -> None:
        self.id = id
        self.name = name
        self.state = 0
        self.events: list = events
        self.delta = delta
        if self.events:
            last_event: TimeEvent = self.events[-1]
            if last_event.type == TimeEventType.START:
                self.state = 1

    def get_delta_str(self) -> str:
        return str(self.delta).split(".")[0]

    def __repr__(self) -> str:
        return f"(id: {self.id}, name: {self.name}, state:{self.state}, events:{self.events})"

    def __str__(self) -> str:
        return self.__repr__()
