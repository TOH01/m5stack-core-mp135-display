import theme
from structures.dataclasses import Color, IconLayer, Rect
from widgets.renderer import Renderer
from widgets.widget import Widget


class Icon(Widget):
    def __init__(self, rect: Rect, layers: list[IconLayer], bg: Color = theme.Palette.BACKGROUND) -> None:
        super().__init__(rect)
        self.bg = bg
        self.layers = layers

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            renderer.draw_icon(self.get_rect(), self.layers, self.bg)
            self.rerender = False

    def update_icon(self, layers: list[IconLayer]) -> None:
        self.layers = layers
        self.rerender = True
