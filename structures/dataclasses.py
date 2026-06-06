from dataclasses import dataclass

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