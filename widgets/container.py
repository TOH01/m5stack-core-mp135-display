from structures.dataclasses import ContainerStyle, PressEvent, Rect
from widgets.renderer import Renderer
from widgets.widget import Widget


class Container(Widget):
    def __init__(self, rect: Rect, style: ContainerStyle) -> None:
        super().__init__(rect)
        self.widgets: list[Widget] = []
        self.style = style

    def add_widget(self, widget: Widget):
        widget.parent = self
        self.widgets.append(widget)

    def render(self, renderer: Renderer) -> None:
        if self.visible:
            if self.rerender:
                renderer.draw_rect(self.get_rect(), self.style.background)
                self.rerender = False

                for widget in self.widgets:
                    widget.rerender = True

            for widget in self.widgets:
                if widget.rerender:
                    widget.render(renderer)
                    widget.rerender = False

    def on_click(self, event: PressEvent) -> None:
        if self.visible:
            for widget in self.widgets:
                if widget.contains(event.point):
                    widget.on_click(event)
                    return
