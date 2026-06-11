import theme
from structures.dataclasses import LabelStyle, Rect, RectStyle, TextStyle
from widgets.renderer import Renderer
from widgets.widget import Widget


class Label(Widget):
    def __init__(self, rect: Rect, text: str, style: LabelStyle) -> None:
        super().__init__(rect)
        self.text = text
        self.style = style

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            # Clear background to prevent character overlapping
            bg_color = self.style.bg if self.style.bg is not None else theme.BG
            renderer.draw_rect(rect, RectStyle(fill=bg_color))
            renderer.draw_text(
                rect,
                self.text,
                TextStyle(
                    color=self.style.color,
                    preset=self.style.preset,
                    alignment=self.style.alignment,
                    tracking=self.style.tracking,
                ),
            )
            self.rerender = False

    def update_text(self, text: str):
        self.text = text
        self.rerender = True
