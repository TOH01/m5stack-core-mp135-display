from structures.dataclasses import ContainerStyle, Rect, RectStyle
from widgets.container import Container


class BottomBar(Container):
    def __init__(self) -> None:
        self.rect = Rect(0, 240 - 25, 320, 25)
        self.style = ContainerStyle(RectStyle((30, 30, 35)))
        super().__init__(self.rect, self.style)
