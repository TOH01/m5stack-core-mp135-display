from structures.dataclasses import Rect, Point
from widgets.utils import is_inside

class Widget:
    def __init__(self, rect: Rect) -> None:
        self.rect = rect
        self.rerender = True

    def contains(self, point : Point) -> bool:
        return is_inside(point, self.rect)
    
    def render(self) -> None:
        pass

    def on_click(self) -> None:
        pass

    def on_swipe(self) -> None:
        pass
