import theme
from structures.dataclasses import Rect
from widgets.clock import Clock
from widgets.container import Container
from widgets.label import Label


class TopBar(Container):
    def __init__(self) -> None:
        self.rect = Rect(0, 0, 320, 30)
        self.style = theme.TRANSPARENT_CONTAINER
        super().__init__(self.rect, self.style)

        self.construct_title()
        self.construct_clock()

    def construct_title(self) -> None:
        # Height 30, v-centered text inside Label
        self.title_widget = Label(
            Rect(13, 0, 160, 30),
            "SYSTEM",
            theme.LABEL_TITLE,
        )
        self.add_widget(self.title_widget)

    def construct_clock(self) -> None:
        # Width 52, height 20, v-centered in TopBar (y=5 to y=25)
        # Ends at 255 + 52 = 307
        self.clock_widget = Clock(Rect(255, 5, 52, 20), theme.TRANSPARENT_CONTAINER)
        self.add_widget(self.clock_widget)

    def update_title(self, text: str) -> None:
        self.title_widget.update_text(text)
