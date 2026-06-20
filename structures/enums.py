from enum import Enum, IntEnum


class TouchEvent(IntEnum):
    UP   = 0
    DOWN = 1


class Direction(Enum):
    UP    = "up"
    DOWN  = "down"
    LEFT  = "left"
    RIGHT = "right"


class WeatherCondition(Enum):
    CLEAR         = "clear"
    PARTLY_CLOUDY = "partly_cloudy"
    CLOUDY        = "cloudy"
    RAIN          = "rain"
    SNOW          = "snow"
    FOG           = "fog"
    THUNDERSTORM  = "thunderstorm"


class TextPreset(Enum):
    HEADING     = "heading"
    BODY        = "body"
    VALUE       = "value"
    DISPLAY     = "display"
    SUBHEAD     = "subhead"
    ICON        = "icon"
    ICON_MEDIUM = "icon_medium"
    ICON_LARGE  = "icon_large"


class TextAlignment(Enum):
    LEFT   = "left"
    CENTER = "center"
    RIGHT  = "right"
