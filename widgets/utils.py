from structures.dataclasses import Rect, Point

def is_inside(point: Point, rect: Rect):
    return (rect.x <= point.x <= rect.x + rect.w) and (rect.y <= point.y <= rect.y + rect.h)