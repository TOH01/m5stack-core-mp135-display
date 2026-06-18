import theme
from structures.dataclasses import Rect
from widgets.container import Container
from widgets.menu_indicator import MenuIndicator


class BottomBar(Container):
    def __init__(self) -> None:
        self.rect = Rect(0, theme.Spacing.SCREEN_H - theme.Spacing.BAR_HEIGHT, theme.Spacing.SCREEN_W, theme.Spacing.BAR_HEIGHT)
        self.style = theme.surface_style()
        super().__init__(self.rect, self.style)

        self.construct_menu_indicator()

    def construct_menu_indicator(self) -> None:
        self.menu_indicator = MenuIndicator(Rect(120, 7, 80, 13), 4)
        self.add_widget(self.menu_indicator)
