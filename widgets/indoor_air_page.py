import theme
from structures.dataclasses import CircleStyle, LabelStyle, Point, Rect, RectStyle, TextStyle
from structures.enums import TextAlignment, TextPreset
from widgets.container import Container
from widgets.label import Label
from widgets.renderer import Renderer
from widgets.widget import Widget


class AirCellWidget(Widget):
    def __init__(
        self,
        rect: Rect,
        cx: int,
        cy: int,
        label: str,
        val: str,
        unit: str,
        status: str,
        dot_color,
    ) -> None:
        super().__init__(rect)
        self.cx = cx
        self.cy = cy
        self.label = label
        self.val = val
        self.unit = unit
        self.status = status
        self.dot_color = dot_color

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            # Clear background first to avoid text overlap
            renderer.draw_rect(rect, RectStyle(fill=theme.BG))
            y_start = rect.y + 3
            
            # 1. Header line: dot 5Ø + 5px gap + label
            font_label = theme.FONT_MAP[TextPreset.MICRO_LABEL]
            label_w = sum(font_label.getlength(c) for c in self.label) + (len(self.label) - 1) * 1
            
            total_header_w = 5 + 5 + label_w
            header_start_x = self.cx - total_header_w / 2
            
            # Draw dot
            dot_center = Point(int(header_start_x + 2), int(y_start + 5))
            renderer.draw_circle(dot_center, 2, CircleStyle(fill=self.dot_color))
            
            # Draw label
            label_rect = Rect(int(header_start_x + 10), int(y_start), int(label_w) + 2, 12)
            renderer.draw_text(
                label_rect,
                self.label,
                TextStyle(
                    color=theme.SUB,
                    preset=TextPreset.MICRO_LABEL,
                    alignment=TextAlignment.LEFT,
                    tracking=1,
                ),
            )
            
            # 2. Value + Unit (baseline aligned)
            font_val = theme.FONT_MAP[TextPreset.AIR_CELL_VALUE]
            font_unit = theme.FONT_MAP[TextPreset.UNIT]
            
            val_w = font_val.getlength(self.val)
            unit_w = font_unit.getlength(self.unit)
            total_val_w = val_w + 3 + unit_w
            val_start_x = self.cx - total_val_w / 2
            
            val_rect_y = y_start + 18
            y_baseline = val_rect_y + 19
            
            renderer.draw.text(
                (val_start_x, y_baseline), self.val, fill=theme.TEXT, font=font_val, anchor="ls"
            )
            renderer.draw.text(
                (val_start_x + val_w + 3, y_baseline),
                self.unit,
                fill=theme.SUB,
                font=font_unit,
                anchor="ls",
            )
            
            # 3. Status text (centered)
            status_rect = Rect(self.cx - 60, y_start + 45, 120, 12)
            renderer.draw_text(
                status_rect,
                self.status,
                TextStyle(
                    color=theme.FAINT, preset=TextPreset.META_STATUS, alignment=TextAlignment.CENTER
                ),
            )
            
            renderer.dirty_regions.append(rect)
            self.rerender = False


class IndoorAirPage(Container):
    def __init__(self) -> None:
        super().__init__(Rect(0, 0, 320, 240), theme.TRANSPARENT_CONTAINER)
        self.construct_widgets()

    def construct_widgets(self) -> None:
        # 2x2 Grid (Centers: x ≈ 86, 234; y ≈ 75, 150)
        # Bounding box width = 120, height = 64
        # Center x=86 -> start x = 26. Center x=234 -> start x = 174
        # Center y=75 -> start y = 43. Center y=150 -> start y = 118
        
        # Row 1: CO₂ (612 ppm, Good · ventilated, green) & IAQ (42 / 500, Excellent, green)
        self.add_widget(
            AirCellWidget(
                Rect(26, 43, 120, 64),
                86,
                75,
                "CO₂",
                "612",
                "ppm",
                "Good · ventilated",
                theme.GOOD,
            )
        )
        self.add_widget(
            AirCellWidget(
                Rect(174, 43, 120, 64),
                234,
                75,
                "IAQ",
                "42",
                "/ 500",
                "Excellent",
                theme.GOOD,
            )
        )

        # Row 2: Temp (22.4 °C, Comfortable, green) & Hum (38 %, Slightly dry, orange)
        self.add_widget(
            AirCellWidget(
                Rect(26, 118, 120, 64),
                86,
                150,
                "TEMP",
                "22.4",
                "°C",
                "Comfortable",
                theme.GOOD,
            )
        )
        self.add_widget(
            AirCellWidget(
                Rect(174, 118, 120, 64),
                234,
                150,
                "HUM",
                "38",
                "%",
                "Slightly dry",
                theme.WARN,
            )
        )

        # Footer (y ≈ 216, left x13, right x307)
        label_footer_left = theme.LABEL_SUB
        label_footer_right = LabelStyle(
            color=theme.FAINT, preset=TextPreset.META_STATUS, alignment=TextAlignment.RIGHT
        )
        self.add_widget(Label(Rect(13, 206, 140, 12), "BME688", label_footer_left))
        self.add_widget(Label(Rect(167, 206, 140, 12), "updated 20 s ago", label_footer_right))
