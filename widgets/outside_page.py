import math
import theme
from structures.dataclasses import LabelStyle, Rect, TextStyle
from structures.enums import TextAlignment, TextPreset
from widgets.container import Container
from widgets.label import Label
from widgets.renderer import Renderer
from widgets.widget import Widget


# Weather Icon Drawing Helpers
def draw_sun(draw, cx: int, cy: int, r: int, color=theme.WARN) -> None:
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    ray_len = max(2, r // 2)
    num_rays = 8
    for i in range(num_rays):
        angle = i * (2 * math.pi / num_rays)
        x1 = cx + (r + 1.5) * math.cos(angle)
        y1 = cy + (r + 1.5) * math.sin(angle)
        x2 = cx + (r + 1.5 + ray_len) * math.cos(angle)
        y2 = cy + (r + 1.5 + ray_len) * math.sin(angle)
        draw.line((int(x1), int(y1), int(x2), int(y2)), fill=color, width=1)


def draw_cloud(draw, cx: int, cy: int, w: int, h: int, color=(126, 138, 153)) -> None:
    # 3-circle flat bottom cloud
    base_y = cy + h // 2
    r1 = h // 2
    r2 = int(h * 0.7)
    r3 = int(h * 0.55)
    
    # Left bump
    draw.ellipse((cx - w // 2, base_y - 2 * r1, cx - w // 2 + 2 * r1, base_y), fill=color)
    # Middle bump
    draw.ellipse((cx - w // 4, base_y - 2 * r2, cx + w // 4, base_y), fill=color)
    # Right bump
    draw.ellipse((cx + w // 2 - 2 * r3, base_y - 2 * r3, cx + w // 2, base_y), fill=color)
    # Bottom rect fill
    draw.rectangle((cx - w // 2 + r1, base_y - r1, cx + w // 2 - r3, base_y), fill=color)


def draw_rain_cloud(draw, cx: int, cy: int, w: int, h: int, color=(126, 138, 153), rain_color=(91, 201, 138)) -> None:
    cloud_cy = cy - 2
    draw_cloud(draw, cx=cx, cy=cloud_cy, w=w, h=h, color=color)
    
    # Rain drops
    rain_y1 = cloud_cy + h // 2 + 1
    rain_y2 = rain_y1 + 3
    draw.line((cx - 3, rain_y1, cx - 3, rain_y2), fill=rain_color, width=1)
    draw.line((cx, rain_y1 + 1, cx, rain_y2 + 1), fill=rain_color, width=1)
    draw.line((cx + 3, rain_y1, cx + 3, rain_y2), fill=rain_color, width=1)


class WeatherGlyphWidget(Widget):
    def __init__(self, rect: Rect, glyph_type: str, size: int) -> None:
        super().__init__(rect)
        self.glyph_type = glyph_type
        self.size = size

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            cx = rect.x + rect.w // 2
            cy = rect.y + rect.h // 2
            
            if self.glyph_type == "sun":
                draw_sun(renderer.draw, cx, cy, self.size // 3)
            elif self.glyph_type == "cloud":
                draw_cloud(renderer.draw, cx, cy, self.size, int(self.size * 0.7))
            elif self.glyph_type == "rain":
                draw_rain_cloud(renderer.draw, cx, cy, self.size, int(self.size * 0.7))
            elif self.glyph_type == "partly_cloudy":
                # Sun in top-left, Cloud in bottom-right
                sun_cx = cx - 4
                sun_cy = cy - 4
                cloud_cx = cx + 4
                cloud_cy = cy + 4
                draw_sun(renderer.draw, sun_cx, sun_cy, self.size // 4)
                draw_cloud(renderer.draw, cloud_cx, cloud_cy, int(self.size * 0.8), int(self.size * 0.55))
            
            renderer.dirty_regions.append(rect)
            self.rerender = False


class OutsideHeroWidget(Widget):
    def __init__(self, rect: Rect, temp: str, condition: str) -> None:
        super().__init__(rect)
        self.temp = temp
        self.condition = condition

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            font_hero = theme.FONT_MAP[TextPreset.HERO]
            font_unit = theme.FONT_MAP[TextPreset.SOCKET_WATTS]  # ~16px
            
            val_w = font_hero.getlength(self.temp)
            unit_text = "°C"
            y_baseline = rect.y + 34
            
            # Draw temperature hero at x15
            renderer.draw.text((rect.x, y_baseline), self.temp, fill=theme.TEXT, font=font_hero, anchor="ls")
            # Draw unit °C on the same baseline
            renderer.draw.text((rect.x + val_w + 3, y_baseline), unit_text, fill=theme.SUB, font=font_unit, anchor="ls")
            
            renderer.dirty_regions.append(rect)
            self.rerender = False


class TomorrowFooterWidget(Widget):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            # Left: "TOMORROW"
            label_style = theme.LABEL_MICRO
            renderer.draw_text(
                Rect(rect.x, rect.y, 100, rect.h),
                "TOMORROW",
                TextStyle(color=theme.SUB, preset=TextPreset.MICRO_LABEL, tracking=1)
            )
            
            # Right: rain cloud icon + hi (14°) + lo ( / 9°)
            font_temp = theme.FONT_MAP[TextPreset.HOUR_TEMP]
            
            lo_text = " / 9°"
            hi_text = "14°"
            
            lo_w = font_temp.getlength(lo_text)
            hi_w = font_temp.getlength(hi_text)
            
            # Right-aligned from x=307
            rx = rect.x + rect.w  # 307
            y_baseline = rect.y + rect.h - 2
            
            # Draw lo
            renderer.draw.text((rx, y_baseline), lo_text, fill=theme.FAINT, font=font_temp, anchor="ls")
            # Draw hi
            renderer.draw.text((rx - lo_w - 2, y_baseline), hi_text, fill=theme.TEXT, font=font_temp, anchor="ls")
            
            # Draw icon (12px rain cloud) to the left of hi text
            icon_cx = int(rx - lo_w - 2 - hi_w - 6 - 6)
            icon_cy = rect.y + rect.h // 2
            draw_rain_cloud(renderer.draw, icon_cx, icon_cy, 12, 8)
            
            renderer.dirty_regions.append(rect)
            self.rerender = False


class OutsidePage(Container):
    def __init__(self) -> None:
        super().__init__(Rect(0, 0, 320, 240), theme.TRANSPARENT_CONTAINER)
        self.construct_widgets()

    def construct_widgets(self) -> None:
        # Hero current temp (starts at x=15, top y=36, height=38)
        self.add_widget(OutsideHeroWidget(Rect(15, 36, 120, 38), "17", "Partly cloudy · feels 15°"))
        
        # Condition line at y=78
        self.add_widget(Label(Rect(15, 78, 200, 12), "Partly cloudy · feels 15°", theme.LABEL_SUB))
        
        # Condition icon on right side at x=262, y=40, block size 44x36
        self.add_widget(WeatherGlyphWidget(Rect(262, 40, 44, 36), "partly_cloudy", 28))

        # Hourly strip: 5 columns from x=13 to 307. Region width = 294. Column width = 58.
        # Centers at x = 42, 101, 160, 219, 278.
        # Hourly stack y center is 137, stack height = 45 -> starts at y=115.
        hours = [
            ("15", "sun", "17°", 42),
            ("16", "cloud", "16°", 101),
            ("17", "cloud", "15°", 160),
            ("18", "rain", "13°", 219),
            ("19", "rain", "12°", 278),
        ]
        
        label_hour_time = LabelStyle(
            color=theme.FAINT, preset=TextPreset.MICRO_LABEL, alignment=TextAlignment.CENTER
        )
        label_hour_temp = LabelStyle(
            color=theme.TEXT, preset=TextPreset.HOUR_TEMP, alignment=TextAlignment.CENTER
        )
        
        for time_str, icon_type, temp_str, cx in hours:
            col_x = cx - 29
            # Time label
            self.add_widget(Label(Rect(col_x, 115, 58, 12), time_str, label_hour_time))
            # Icon
            self.add_widget(WeatherGlyphWidget(Rect(col_x, 130, 58, 16), icon_type, 14))
            # Temp label
            self.add_widget(Label(Rect(col_x, 151, 58, 12), temp_str, label_hour_temp))

        # Tomorrow footer (y ≈ 206 to 218)
        self.add_widget(TomorrowFooterWidget(Rect(13, 206, 294, 12)))
