from typing import Union
from enum import Enum
from dataclasses import dataclass


class EventType(Enum):
    DIAL_EVENT = 0
    HANDSET_EVENT = 1


class HandsetState(Enum):
    HUNG_UP = 0
    PICKED_UP = 1


@dataclass(frozen=True)
class DialEvent:
    type: EventType
    data: Union[HandsetState, int]
