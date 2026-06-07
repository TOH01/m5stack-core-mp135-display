from structures.dataclasses import ContainerStyle, PressEvent, Rect, SwipeEvent
from widgets.renderer import Renderer
from widgets.widget import Widget


class Container(Widget):
    def __init__(self, rect: Rect, style: ContainerStyle) -> None:
        super().__init__(rect)
        self.widgets = []
        self.style = style

    def add_widget(self, widget: Widget):
        widget.parent = self
        self.widgets.append(widget)

    def render(self, renderer: Renderer) -> None:
        renderer.draw_rect(self.get_rect(), self.style.background)

    def on_click(self, event: PressEvent) -> None:
        pass

    def on_swipe(self, event: SwipeEvent) -> None:
        pass
