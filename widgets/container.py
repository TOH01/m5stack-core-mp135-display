from structures.dataclasses import Rect, PressEvent, SwipeEvent
from widgets.renderer import Renderer
from widgets.widget import Widget

class Container(Widget):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)
        self.widgets = []

    def add_widget(self, widget: Widget):
        widget.parent = self
        self.widgets.append(widget)

    def render(self, renderer: Renderer) -> None:
        pass

    def on_click(self, event: PressEvent) -> None:
        pass

    def on_swipe(self, event: SwipeEvent) -> None:
        pass
