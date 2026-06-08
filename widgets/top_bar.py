from structures.dataclasses import ContainerStyle, LabelStyle, Rect, RectStyle, TextPreset
from widgets.clock import Clock
from widgets.container import Container
from widgets.label import Label


class TopBar(Container):
    def __init__(self) -> None:
        self.rect = Rect(0, 0, 320, 25)
        self.style = ContainerStyle(RectStyle((30, 30, 35)))
        super().__init__(self.rect, self.style)

        self.construct_title()
        self.construct_clock()

    def construct_title(self) -> None:
        self.title_widget = Label(
            Rect(8, 5, (240 // 2), 25 - 5),
            "Placeholder",
            LabelStyle((240, 240, 240), TextPreset.HEADING, (30, 30, 35)),
        )
        self.add_widget(self.title_widget)

    def construct_clock(self) -> None:
        self.clock_widget = Clock(Rect(260, 5, 60, 20), ContainerStyle(RectStyle((30, 30, 35))))
        self.add_widget(self.clock_widget)

    def update_title(self, text: str) -> None:
        self.title_widget.update_text(text)
