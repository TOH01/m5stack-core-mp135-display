from structures.dataclasses import Rect
from widgets.widget import Widget

class Container(Widget):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)