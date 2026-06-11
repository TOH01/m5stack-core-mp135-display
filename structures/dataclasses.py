from dataclasses import dataclass

from structures.enums import Direction, TextAlignment, TextPreset


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int


@dataclass
class RectStyle:
    fill: tuple[int, int, int] = (0, 0, 0)
    outline: tuple[int, int, int] | None = None
    outline_width: int = 1
    radius: int = 0


@dataclass
class ContainerStyle:
    background: RectStyle


@dataclass
class TextStyle:
    color: tuple[int, int, int]
    preset: TextPreset
    alignment: TextAlignment = TextAlignment.LEFT


@dataclass
class LabelStyle:
    color: tuple[int, int, int]
    preset: TextPreset
    bg: tuple[int, int, int] = (0, 0, 0)
    alignment: TextAlignment = TextAlignment.LEFT


@dataclass
class Point:
    x: int
    y: int


@dataclass
class CircleStyle:
    fill: tuple[int, int, int] = (0, 0, 0)
    outline: tuple[int, int, int] | None = None
    outline_width: int = 1


@dataclass
class LineStyle:
    color: tuple[int, int, int] = (0, 0, 0)
    width: int = 1


@dataclass
class PressEvent:
    point: Point


@dataclass
class SwipeEvent:
    direction: Direction
