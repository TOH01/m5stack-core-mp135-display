from dataclasses import dataclass
from structures.enums import Direction

@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

@dataclass
class Point:
    x: int
    y: int

@dataclass
class PressEvent:
    points: Point

@dataclass
class SwipeEvent:
    directon: Direction