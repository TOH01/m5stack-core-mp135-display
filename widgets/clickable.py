from structures.dataclasses import PressEvent, Rect
from widgets.widget import Widget
from typing import Callable

class Clickable(Widget):
    def __init__(self, rect: Rect, callback: Callable) -> None:
        super().__init__(rect)
        self.callback = callback

    def on_click(self, event: PressEvent) -> None:
        if self.callback:
            self.callback()