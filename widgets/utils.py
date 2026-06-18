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

def _carve(rect: Rect, hole: Rect) -> list[Rect]:
    ix, iy = max(rect.x, hole.x), max(rect.y, hole.y)
    ir, ib = min(rect.x + rect.w, hole.x + hole.w), min(rect.y + rect.h, hole.y + hole.h)
    if ix >= ir or iy >= ib:
        return [rect]

    pieces: list[Rect] = []
    if rect.y < iy:
        pieces.append(Rect(rect.x, rect.y, rect.w, iy - rect.y))
    if ib < rect.y + rect.h:
        pieces.append(Rect(rect.x, ib, rect.w, rect.y + rect.h - ib))
    if rect.x < ix:
        pieces.append(Rect(rect.x, iy, ix - rect.x, ib - iy))
    if ir < rect.x + rect.w:
        pieces.append(Rect(ir, iy, rect.x + rect.w - ir, ib - iy))
    return pieces

def subtract_regions(regions: list[Rect], holes: list[Rect]) -> list[Rect]:
    result = list(regions)
    for hole in holes:
        carved: list[Rect] = []
        for rect in result:
            carved.extend(_carve(rect, hole))
        result = carved
    return result
