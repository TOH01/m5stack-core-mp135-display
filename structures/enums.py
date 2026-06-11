from enum import Enum, IntEnum


class TouchEvent(IntEnum):
    UP = 0
    DOWN = 1


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class TextPreset(Enum):
    HERO = "hero"
    COLUMN_VALUE = "column_value"
    AIR_CELL_VALUE = "air_cell_value"
    SOCKET_WATTS = "socket_watts"
    FOOTER_STAT = "footer_stat"
    HOUR_TEMP = "hour_temp"
    TIME = "time"
    SCREEN_TITLE = "screen_title"
    UNIT = "unit"
    MICRO_LABEL = "micro_label"
    META_STATUS = "meta_status"


class TextAlignment(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"
