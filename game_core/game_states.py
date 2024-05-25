from enum import Enum


class State(Enum):
    DRAW = 'DRAW'
    CROSS_WON = 'CROSS_WON'
    ZERO_WON = 'ZERO_WON'
    IN_PROGRESS = 'IN_PROGRESS'
