import theme
from application.timer_event import TimerEvent
from structures.dataclasses import ForecastEntry, PressEvent, Rect, WeatherReading
from structures.enums import WeatherCondition
from widgets.container import Container
from widgets.icon import Icon
from widgets.label import Label

ROTATE_INTERVAL_MS = 4000


class OutdoorWeatherMenu(Container):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect, theme.transparent_container_style())
        margin = theme.Spacing.MARGIN

        self.temperature = Label(Rect(margin, 8, 180, 70), "--", theme.hero_value_style())
        self.caption     = Label(Rect(margin + 2, 84, rect.w - 2 * margin, 20), "--", theme.caption_style())
        self.icon        = Icon(Rect(rect.w - margin - 78, 6, 78, 78), theme.weather_icon_layers(WeatherCondition.CLOUDY))

        col_w = (rect.w - 2 * margin) // 2
        self.cells: list[tuple[Icon, Label, Label]] = []
        for i in range(2):
            x = margin + i * col_w
            cell_icon  = Icon(Rect(x + 8, 112, 52, 64), theme.weather_icon_layers(WeatherCondition.CLOUDY))
            cell_label = Label(Rect(x + 66, 120, col_w - 72, 20), "--", theme.caption_style())
            cell_temp  = Label(Rect(x + 66, 142, col_w - 72, 28), "--", theme.value_style())
            self.cells.append((cell_icon, cell_label, cell_temp))

        for widget in (self.temperature, self.caption, self.icon):
            self.add_widget(widget)
        for cell in self.cells:
            for widget in cell:
                self.add_widget(widget)

        self._hourly: list[ForecastEntry] = []
        self._daily: list[ForecastEntry] = []
        self._show_hourly = True
        self.rotate_timer = TimerEvent(ROTATE_INTERVAL_MS, self._toggle_strip)
        self.add_timer(self.rotate_timer)

    def set_reading(self, reading: WeatherReading) -> None:
        self.temperature.update_text(f"{reading.temperature_c:.0f}°")
        self.caption.update_text(f"{theme.weather_label(reading.condition)} · feels {reading.feels_like_c:.0f}°")
        self.icon.update_icon(theme.weather_icon_layers(reading.condition))
        self._hourly = reading.hourly
        self._daily = reading.daily
        self._render_strip()

    def on_click(self, event: PressEvent) -> None:
        self._toggle_strip()
        self.rotate_timer.reset()

    def _toggle_strip(self) -> None:
        self._show_hourly = not self._show_hourly
        self._render_strip()

    def _render_strip(self) -> None:
        entries = self._hourly if self._show_hourly else self._daily
        for (cell_icon, cell_label, cell_temp), entry in zip(self.cells, entries):
            cell_icon.update_icon(theme.weather_icon_layers(entry.condition))
            cell_label.update_text(entry.label)
            cell_temp.update_text(f"{entry.temperature_c:.0f}°")
