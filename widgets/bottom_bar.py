import theme
from structures.dataclasses import Rect
from widgets.container import Container
from widgets.menu_indicator import MenuIndicator


class BottomBar(Container):
    def __init__(self) -> None:
        self.rect = Rect(0, 240 - 25, 320, 25)
        self.style = theme.TRANSPARENT_CONTAINER
        super().__init__(self.rect, self.style)

        self.construct_menu_indicator()

    def construct_menu_indicator(self):
        self.menu_indicator = MenuIndicator(Rect(120, 7, 80, 13), 4)
        self.add_widget(self.menu_indicator)
