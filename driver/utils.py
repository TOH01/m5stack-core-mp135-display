import math

from structures.dataclasses import Point
from structures.enums import Direction


def map_brightness(brightness: int) -> int:
    return math.ceil(brightness / 2) + 50


def get_distance(p1: Point, p2: Point) -> float:
    return math.hypot(p2.x - p1.x, p2.y - p1.y)


def get_swipe_direction(start: Point, end: Point) -> Direction:
    dx = end.x - start.x
    dy = end.y - start.y

    if abs(dx) > abs(dy):
        return Direction.RIGHT if dx > 0 else Direction.LEFT
    else:
        return Direction.DOWN if dy > 0 else Direction.UP
