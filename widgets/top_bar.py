from structures.dataclasses import Rect
from widgets.container import Container

class TopBar(Container):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)