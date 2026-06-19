import theme
from structures.dataclasses import Rect
from widgets.clock import Clock
from widgets.container import Container
from widgets.label import Label


class TopBar(Container):
    def __init__(self) -> None:
        self.rect = Rect(0, 0, theme.Spacing.SCREEN_W, theme.Spacing.BAR_HEIGHT)
        self.style = theme.menu_background_style()
        super().__init__(self.rect, self.style)

        self.construct_title()
        self.construct_clock()

    def construct_title(self) -> None:
        self.title_widget = Label(Rect(theme.Spacing.PADDING, 5, (240 // 2), theme.Spacing.BAR_HEIGHT - 5), "Placeholder", theme.top_bar_text_style())
        self.add_widget(self.title_widget)

    def construct_clock(self) -> None:
        self.clock_widget = Clock(Rect(260, 5, 60, 20), theme.menu_background_style())
        self.add_widget(self.clock_widget)

    def update_title(self, text: str) -> None:
        self.title_widget.update_text(text)
