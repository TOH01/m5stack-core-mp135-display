from enum import Enum, IntEnum

class TouchEvent(IntEnum):
    UP = 0
    DOWN = 1

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"