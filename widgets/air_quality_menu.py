import theme
from structures.dataclasses import IconLayer, Rect, SensorReading
from widgets.container import Container
from widgets.layout import Layout1, Layout3, Layout4


class AirQualityMenu(Container):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect, theme.transparent_container_style())
        self.layout_1              = Layout1(rect)
        self.co2, self.co2_caption = self.layout_1.get_layout()

        self.layout3                  = Layout3(rect)
        self.temp_icon, self.hum_icon = self.layout3.get_layout()

        self.layout4                    = Layout4(rect)
        self.temperature, self.humidity = self.layout4.get_layout()

        for widget in (self.co2, self.co2_caption, self.temp_icon, self.temperature, self.hum_icon, self.humidity):
            self.add_widget(widget)

        self.temp_icon.update_icon([IconLayer(theme.Icon.TEMPERATURE, theme.Palette.WARM, 1, 0, 0)])
        self.hum_icon.update_icon([IconLayer(theme.Icon.HUMIDITY, theme.Palette.COOL, 1, 0, 0)])

    def set_reading(self, reading: SensorReading) -> None:
        band = theme.band_for(reading.co2_ppm, theme.CO2_BANDS)
        self.co2.update_text(str(reading.co2_ppm), band.color)
        self.co2_caption.update_text(f"CO₂ PPM · {band.label}")
        self.temperature.update_text(f"{reading.temperature_c:.1f}°")
        self.humidity.update_text(f"{reading.humidity}%")
