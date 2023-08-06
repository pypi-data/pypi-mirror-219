from enum import Enum
from datetime import datetime


class TimeEventType(Enum):
    STOP = 0
    START = 1


class TimeEvent:
    created: datetime
    type: TimeEventType

    def __init__(self, type: TimeEventType, created: datetime = datetime.now()) -> None:
        self.type = type
        self.created = created

    def __repr__(self) -> str:
        return f"event:({self.type}, {self.created})"

    def __str__(self) -> str:
        return self.__repr__()
