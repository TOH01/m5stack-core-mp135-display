import theme
from structures.dataclasses import IconLayer, Rect, SensorReading
from widgets.container import Container
from widgets.icon import Icon
from widgets.label import Label


class AirQualityMenu(Container):
    def __init__(self, rect: Rect) -> None:
        super().__init__(rect, theme.transparent_container_style())
        margin = theme.Spacing.MARGIN
        padding = theme.Spacing.PADDING

        self.co2         = Label(Rect(margin, 26, rect.w - 2 * margin, 70), "--", theme.hero_value_style())
        self.co2_caption = Label(Rect(margin + 2, 100, rect.w - 2 * margin, 22), "CO₂ PPM", theme.caption_style())

        row_y = 140
        self.temp_icon    = Icon(Rect(margin - 5, row_y, 32, 36), [IconLayer(theme.Icon.TEMPERATURE, theme.Palette.WARM, 1, 0, 0)])
        self.temperature  = Label(Rect(padding + 38 - 3, row_y, 70, 36), "--", theme.value_style())
        self.hum_icon     = Icon(Rect(110 + margin + padding - 3, row_y, 32, 36), [IconLayer(theme.Icon.HUMIDITY, theme.Palette.COOL, 1, 0, 0)])
        self.humidity     = Label(Rect(110 + margin + 36 + padding - 3, row_y, 65, 36), "--", theme.value_style())

        for widget in (self.co2, self.co2_caption, self.temp_icon, self.temperature, self.hum_icon, self.humidity):
            self.add_widget(widget)

    def set_reading(self, reading: SensorReading) -> None:
        band = theme.band_for(reading.co2_ppm, theme.CO2_BANDS)
        self.co2.update_text(str(reading.co2_ppm), band.color)
        self.co2_caption.update_text(f"CO₂ PPM · {band.label}")
        self.temperature.update_text(f"{reading.temperature_c:.1f}°")
        self.humidity.update_text(f"{reading.humidity}%")
