import theme
from structures.dataclasses import LabelStyle, Rect, RectStyle, TextStyle
from structures.enums import TextAlignment, TextPreset
from widgets.container import Container
from widgets.icons import get_tinted_icon
from widgets.label import Label
from widgets.renderer import Renderer
from widgets.widget import Widget


class WeatherGlyphWidget(Widget):
    def __init__(self, rect: Rect, glyph_type: str, size: int) -> None:
        super().__init__(rect)
        self.glyph_type = glyph_type
        self.size = size

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            # Clear background
            renderer.draw_rect(rect, RectStyle(fill=theme.BG))
            
            w, h = rect.w, rect.h
            
            # Use native colors by passing color=None
            if self.glyph_type in ["sun", "cloud", "rain", "partly_cloudy"]:
                icon = get_tinted_icon(self.glyph_type, (self.size, self.size), None)
                x = rect.x + (w - icon.width) // 2
                y = rect.y + (h - icon.height) // 2
                renderer.canvas.paste(icon, (x, y), icon)
            
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
            # Clear background
            renderer.draw_rect(rect, RectStyle(fill=theme.BG))
            
            font_hero = theme.FONT_MAP[TextPreset.HERO]
            font_unit = theme.FONT_MAP[TextPreset.SOCKET_WATTS]
            
            val_w = font_hero.getlength(self.temp)
            unit_text = "°C"
            y_baseline = rect.y + 34
            
            renderer.draw.text((rect.x, y_baseline), self.temp, fill=theme.TEXT, font=font_hero, anchor="ls")
            renderer.draw.text((rect.x + val_w + 3, y_baseline), unit_text, fill=theme.SUB, font=font_unit, anchor="ls")
            
            renderer.dirty_regions.append(rect)
            self.rerender = False


class TomorrowFooterWidget(Widget):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect)

    def render(self, renderer: Renderer) -> None:
        if self.rerender:
            rect = self.get_rect()
            # Clear background
            renderer.draw_rect(rect, RectStyle(fill=theme.BG))
            
            # Left: "TOMORROW"
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
            
            rx = rect.x + rect.w
            y_baseline = rect.y + rect.h - 2
            
            renderer.draw.text((rx, y_baseline), lo_text, fill=theme.FAINT, font=font_temp, anchor="rs")
            renderer.draw.text((rx - lo_w - 2, y_baseline), hi_text, fill=theme.TEXT, font=font_temp, anchor="rs")
            
            # Draw rain icon to the left of hi text (size 16) - native color
            icon_w = 16
            icon = get_tinted_icon("rain", (icon_w, icon_w), None)
            icon_x = int(rx - lo_w - 2 - hi_w - 6 - icon.width)
            icon_y = rect.y + (rect.h - icon.height) // 2
            
            renderer.canvas.paste(icon, (icon_x, icon_y), icon)
            
            renderer.dirty_regions.append(rect)
            self.rerender = False


class OutsidePage(Container):
    def __init__(self) -> None:
        super().__init__(Rect(0, 0, 320, 240), theme.TRANSPARENT_CONTAINER)
        self.construct_widgets()

    def construct_widgets(self) -> None:
        self.add_widget(OutsideHeroWidget(Rect(15, 36, 120, 38), "17", "Partly cloudy · feels 15°"))
        self.add_widget(Label(Rect(15, 78, 200, 12), "Partly cloudy · feels 15°", theme.LABEL_SUB))
        
        # Main condition icon (size 30)
        self.add_widget(WeatherGlyphWidget(Rect(262, 40, 44, 36), "partly_cloudy", 30))

        # Hourly strip: 4 columns from x=13 to 307. Region width = 294. Column width = 73.
        # Centers at x = 49, 122, 195, 268.
        # Spaced out for legibility. Icon size is 18px.
        hours = [
            ("15", "sun", "17°", 49),
            ("16", "cloud", "16°", 122),
            ("17", "cloud", "15°", 195),
            ("18", "rain", "13°", 268),
        ]
        
        label_hour_time = LabelStyle(
            color=theme.FAINT, preset=TextPreset.MICRO_LABEL, alignment=TextAlignment.CENTER
        )
        label_hour_temp = LabelStyle(
            color=theme.TEXT, preset=TextPreset.HOUR_TEMP, alignment=TextAlignment.CENTER
        )
        
        for time_str, icon_type, temp_str, cx in hours:
            col_x = cx - 36
            # Spaced y layout: time at 106, icon at 123 (size 18), temp at 148
            self.add_widget(Label(Rect(col_x, 106, 73, 12), time_str, label_hour_time))
            self.add_widget(WeatherGlyphWidget(Rect(col_x, 123, 73, 18), icon_type, 18))
            self.add_widget(Label(Rect(col_x, 148, 73, 12), temp_str, label_hour_temp))

        self.add_widget(TomorrowFooterWidget(Rect(13, 202, 294, 16)))
