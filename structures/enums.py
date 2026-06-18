from enum import Enum, IntEnum


class TouchEvent(IntEnum):
    UP   = 0
    DOWN = 1


class Direction(Enum):
    UP    = "up"
    DOWN  = "down"
    LEFT  = "left"
    RIGHT = "right"


class TextPreset(Enum):
    HEADING = "heading"
    BODY    = "body"


class TextAlignment(Enum):
    LEFT   = "left"
    CENTER = "center"
    RIGHT  = "right"
