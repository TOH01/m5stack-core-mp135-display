from structures.dataclasses import Point, Rect


def is_inside(point: Point, rect: Rect) -> bool:
    return (rect.x <= point.x <= rect.x + rect.w) and (rect.y <= point.y <= rect.y + rect.h)


def contains(outer: Rect, inner: Rect) -> bool:
    return (
        outer.x <= inner.x
        and outer.y <= inner.y
        and inner.x + inner.w <= outer.x + outer.w
        and inner.y + inner.h <= outer.y + outer.h
    )


def fits(child: Rect, parent: Rect) -> bool:
    return (
        child.x >= 0
        and child.y >= 0
        and child.x + child.w <= parent.w
        and child.y + child.h <= parent.h
    )


def merge_regions(regions: list[Rect]) -> list[Rect]:
    merged: list[Rect] = []
    for rect in sorted(regions, key=lambda r: r.w * r.h, reverse=True):
        if not any(contains(kept, rect) for kept in merged):
            merged.append(rect)
    return merged


def clamp(rect: Rect, max_w: int, max_h: int) -> Rect:
    x, y = max(rect.x, 0), max(rect.y, 0)
    return Rect(x, y, min(rect.x + rect.w, max_w) - x, min(rect.y + rect.h, max_h) - y)
