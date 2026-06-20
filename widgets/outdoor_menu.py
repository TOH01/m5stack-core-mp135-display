import theme
from structures.dataclasses import ForecastEntry, Rect, WeatherReading
from widgets.container import Container
from widgets.layout import Layout1, Layout2, Layout3, Layout5


class OutdoorWeatherMenu(Container):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect, theme.transparent_container_style())

        self.layout1                   = Layout1(rect)
        self.temperature, self.caption = self.layout1.get_layout()
        
        self.layout2 = Layout2(rect)
        self.icon    = self.layout2.get_layout()

        self.layout3 = Layout3(rect)
        self.icon_low_left, self.icon_low_right = self.layout3.get_layout()

        self.layout5                                                                           = Layout5(rect)
        self.caption_low_left, self.text_low_left, self.caption_low_right, self.text_low_right = self.layout5.get_layout()

        for widget in (self.temperature, self.caption, self.icon, self.icon_low_left, self.icon_low_right,
                       self.caption_low_left, self.text_low_left, self.caption_low_right, self.text_low_right):
            self.add_widget(widget)

        self._hourly: list[ForecastEntry] = []
        self._daily: list[ForecastEntry]  = []

    def set_forecast_left(self, forecast: ForecastEntry):
        self.icon_low_left.update_icon(theme.weather_icon_layers(forecast.condition))
        self.caption_low_left.update_text(forecast.label)
        self.text_low_left.update_text(f"{forecast.temperature_c:.0f}°")

    def set_forecast_right(self, forecast: ForecastEntry):
        self.icon_low_right.update_icon(theme.weather_icon_layers(forecast.condition))
        self.caption_low_right.update_text(forecast.label)
        self.text_low_right.update_text(f"{forecast.temperature_c:.0f}°")

    def set_reading(self, reading: WeatherReading) -> None:
        self.temperature.update_text(f"{reading.temperature_c:.0f}°")
        self.caption.update_text(f"{theme.weather_label(reading.condition)} · feels {reading.feels_like_c:.0f}°")
        self.icon.update_icon(theme.weather_icon_layers(reading.condition))
        self.set_forecast_left(reading.hourly)
        self.set_forecast_right(reading.daily)
