from dataclasses import dataclass
from typing import NamedTuple

from structures.enums import Direction, TextAlignment, TextPreset, WeatherCondition


class Color(NamedTuple):
    r: int
    g: int
    b: int


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int


@dataclass
class RectStyle:
    fill: Color = Color(0, 0, 0)
    outline: Color | None = None
    outline_width: int = 1
    radius: int = 0


@dataclass
class ContainerStyle:
    background: RectStyle | None


@dataclass
class TextStyle:
    color: Color
    preset: TextPreset
    alignment: TextAlignment = TextAlignment.LEFT


@dataclass
class LabelStyle:
    color: Color
    preset: TextPreset
    bg: Color = Color(0, 0, 0)
    alignment: TextAlignment = TextAlignment.LEFT


@dataclass
class Point:
    x: int
    y: int


@dataclass
class CircleStyle:
    fill: Color = Color(0, 0, 0)
    outline: Color | None = None
    outline_width: int = 1


@dataclass
class LineStyle:
    color: Color = Color(0, 0, 0)
    width: int = 1


@dataclass
class Band:
    color: Color
    lower: float
    label: str


@dataclass
class SensorReading:
    temperature_c: float
    humidity: int
    iaq: int
    co2_ppm: int


@dataclass
class IconLayer:
    codepoint: int
    color: Color
    scale: float
    dx: float
    dy: float
    fill: bool = False


@dataclass
class ForecastEntry:
    label: str
    condition: WeatherCondition
    temperature_c: float


@dataclass
class WeatherReading:
    temperature_c: float
    condition: WeatherCondition
    feels_like_c: float
    hourly: list[ForecastEntry]
    daily: list[ForecastEntry]


@dataclass
class PressEvent:
    point: Point


@dataclass
class SwipeEvent:
    direction: Direction
