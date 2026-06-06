from structures.dataclasses import Rect, Point, PressEvent, SwipeEvent
from widgets.utils import is_inside
from widgets.renderer import Renderer

class Widget:
    def __init__(self, rect: Rect) -> None:
        self.rect = rect
        self.rerender = True
        self.parent: Widget | None = None

    def get_rect(self) -> Rect:
        rect = Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
        if self.parent:
            parent_rect = self.parent.get_rect()
            rect.x = rect.x + parent_rect.x
            rect.y = rect.y + parent_rect.y

        return rect

    def contains(self, point : Point) -> bool:
        return is_inside(point, self.get_rect())
    
    def render(self, renderer: Renderer) -> None:
        pass

    def on_click(self, event: PressEvent) -> None:
        pass

    def on_swipe(self, event: SwipeEvent) -> None:
        pass
