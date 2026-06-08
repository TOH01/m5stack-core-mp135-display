from structures.dataclasses import Point, Rect


def is_inside(point: Point, rect: Rect):
    return (rect.x <= point.x <= rect.x + rect.w) and (rect.y <= point.y <= rect.y + rect.h)


def fits(child: Rect, parent: Rect) -> bool:
    return (
        child.x >= 0
        and child.y >= 0
        and child.x + child.w <= parent.w
        and child.y + child.h <= parent.h
    )
