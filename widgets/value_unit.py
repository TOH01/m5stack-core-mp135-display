import theme
from structures.dataclasses import Rect, RectStyle
from widgets.renderer import Renderer
from widgets.widget import Widget


class ValueUnitWidget(Widget):
    def __init__(
        self,
        rect: Rect,
        val_text: str,
        unit_text: str,
        val_preset,
        unit_preset,
        val_color=theme.TEXT,
        unit_color=theme.SUB,
    ) -> None:
        super().__init__(rect)
        self.val_text = val_text
        self.unit_text = unit_text
        self.val_preset = val_preset
        self.unit_preset = unit_preset
        self.val_color = val_color
        self.unit_color = unit_color

    def update_values(self, val_text: str, val_color=None) -> None:
        self.val_text = val_text
        if val_color is not None:
            self.val_color = val_color
        self.rerender = True

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            # Clear background first to avoid overlapping text
            renderer.draw_rect(rect, RectStyle(fill=theme.BG))
            
            font_val = theme.FONT_MAP[self.val_preset]
            font_unit = theme.FONT_MAP[self.unit_preset]
            
            val_w = font_val.getlength(self.val_text)
            unit_w = font_unit.getlength(self.unit_text)
            total_w = val_w + 3 + unit_w
            
            # Horizontal centering inside rect
            start_x = rect.x + (rect.w - total_w) / 2
            
            # Align baselines: let descent be ~15% of the height
            y_baseline = rect.y + rect.h - max(2, int(rect.h * 0.15))
            
            # Draw using Pillow's draw.text with anchor "ls" (left-baseline)
            renderer.draw.text(
                (start_x, y_baseline),
                self.val_text,
                fill=self.val_color,
                font=font_val,
                anchor="ls",
            )
            renderer.draw.text(
                (start_x + val_w + 3, y_baseline),
                self.unit_text,
                fill=self.unit_color,
                font=font_unit,
                anchor="ls",
            )
            
            renderer.dirty_regions.append(rect)
            self.rerender = False
