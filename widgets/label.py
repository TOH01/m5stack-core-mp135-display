from structures.dataclasses import Rect, LabelStyle, TextStyle, RectStyle
from widgets.widget import Widget
from widgets.renderer import Renderer

class Label(Widget):
    def __init__(self, rect: Rect, text: str, style: LabelStyle) -> None:
        super().__init__(rect)
        self.text = text
        self.style = style

    def render(self, renderer: Renderer) -> None:
        rect = self.get_rect()
        renderer.draw_rect(rect, RectStyle(fill=self.style.bg))
        renderer.draw_text(rect, self.text, TextStyle(
            color=self.style.color, preset=self.style.preset, alignment=self.style.alignment
        ))
