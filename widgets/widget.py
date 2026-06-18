from application.timer_event import TimerEvent
from structures.dataclasses import Point, PressEvent, Rect
from widgets.renderer import Renderer
from widgets.utils import is_inside


class Widget:
    def __init__(self, rect: Rect) -> None:
        self.rect = rect
        self.rerender = True
        self.parent: Widget | None = None
        self.visible = True
        self.active = True
        self.timers: list[TimerEvent] = []

    def get_rect(self) -> Rect:
        rect = Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
        if self.parent:
            parent_rect = self.parent.get_rect()
            rect.x = rect.x + parent_rect.x
            rect.y = rect.y + parent_rect.y

        return rect

    def contains(self, point: Point) -> bool:
        return is_inside(point, self.get_rect())

    def render(self, renderer: Renderer) -> None:
        pass

    def on_click(self, event: PressEvent) -> None:
        pass

    def add_timer(self, timer: TimerEvent) -> None:
        self.timers.append(timer)

    def check_timers(self) -> None:
        if self.timers:
            for timer in self.timers:
                timer.check()
