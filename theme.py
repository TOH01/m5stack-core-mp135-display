from structures.dataclasses import Band, Color, ContainerStyle, IconLayer, LabelStyle, RectStyle
from structures.enums import TextAlignment, TextPreset, WeatherCondition


class Palette:
    BACKGROUND   = Color(18, 18, 20)     # near-black
    SURFACE      = Color(30, 30, 35)     # dark gray
    OVERLAY      = Color(40, 40, 48)     # slate gray
    TEXT_PRIMARY = Color(220, 220, 220)  # off-white
    ACCENT       = Color(255, 255, 255)  # white
    MUTED        = Color(90, 90, 90)     # medium gray

    GOOD     = Color(130, 200, 150)      # pastel green
    MODERATE = Color(230, 205, 140)      # pastel sand
    POOR     = Color(232, 170, 120)      # pastel peach
    BAD      = Color(226, 128, 128)      # pastel rose

    WARM     = Color(233, 138, 138)      # pastel red (temperature)
    COOL     = Color(132, 188, 232)      # pastel blue (humidity)
    DIM      = Color(150, 150, 160)      # icons, secondary text

    SUN      = Color(245, 202, 92)       # sun
    CLOUD    = Color(212, 218, 228)      # cloud body
    RAIN     = Color(120, 175, 235)      # raindrops
    SNOW     = Color(226, 233, 245)      # snowflakes
    BOLT     = Color(247, 206, 96)       # lightning


class Icon:
    TEMPERATURE = 0xE846
    HUMIDITY    = 0xE798
    AIR_QUALITY = 0xF55B
    CO2         = 0xE7B0

    SUN       = 0xE81A
    CLOUD     = 0xF15C
    DROP      = 0xE798
    SNOWFLAKE = 0xED5B
    BOLT      = 0xEA0B
    MIST      = 0xF084
    MOON      = 0xF036


DEFAULT_BAND = Band(Palette.ACCENT, 0, "--")

CO2_BANDS = [Band(Palette.GOOD, 0, "FRESH"), Band(Palette.MODERATE, 800, "FAIR"), Band(Palette.POOR, 1200, "VENTILATE"), Band(Palette.BAD, 2000, "VENTILATE!")]

WEATHER_ICONS = {
    WeatherCondition.CLEAR:         [IconLayer(Icon.SUN, Palette.SUN, 1.0, 0.0, 0.0)],
    WeatherCondition.PARTLY_CLOUDY: [IconLayer(Icon.SUN, Palette.SUN, 0.55, 0.26, -0.24), IconLayer(Icon.CLOUD, Palette.BACKGROUND, 0.96, 0.04, 0.12, fill=1), IconLayer(Icon.CLOUD, Palette.CLOUD, 0.95, 0.04, 0.12)],
    WeatherCondition.CLOUDY:        [IconLayer(Icon.CLOUD, Palette.CLOUD, 1.0, 0.0, 0.0)],
    WeatherCondition.RAIN:          [IconLayer(Icon.CLOUD, Palette.DIM, 0.85, 0.0, -0.16), IconLayer(Icon.DROP, Palette.RAIN, 0.22, -0.22, 0.40), IconLayer(Icon.DROP, Palette.RAIN, 0.22, 0.0, 0.46), IconLayer(Icon.DROP, Palette.RAIN, 0.22, 0.22, 0.40)],
    WeatherCondition.SNOW:          [IconLayer(Icon.CLOUD, Palette.DIM, 0.85, 0.0, -0.16), IconLayer(Icon.SNOWFLAKE, Palette.SNOW, 0.24, -0.22, 0.40), IconLayer(Icon.SNOWFLAKE, Palette.SNOW, 0.24, 0.22, 0.40)],
    WeatherCondition.FOG:           [IconLayer(Icon.CLOUD, Palette.CLOUD, 0.82, 0.0, -0.22), IconLayer(Icon.MIST, Palette.DIM, 0.66, 0.0, 0.34)],
    WeatherCondition.THUNDERSTORM:  [IconLayer(Icon.CLOUD, Palette.DIM, 0.85, 0.0, -0.16), IconLayer(Icon.BOLT, Palette.BOLT, 0.44, 0.0, 0.36)],
}

WEATHER_LABELS = {
    WeatherCondition.CLEAR:         "Clear",
    WeatherCondition.PARTLY_CLOUDY: "Partly cloudy",
    WeatherCondition.CLOUDY:        "Cloudy",
    WeatherCondition.RAIN:          "Rain",
    WeatherCondition.SNOW:          "Snow",
    WeatherCondition.FOG:           "Fog",
    WeatherCondition.THUNDERSTORM:  "Storm",
}


class Spacing:
    SCREEN_W       = 320
    SCREEN_H       = 240
    BAR_HEIGHT     = 25
    PADDING        = 8
    MARGIN         = 16
    OVERLAY_RADIUS = 8


class Indicator:
    DOT_RATIO  = 0.7
    PILL_RATIO = 3.0
    GAP_RATIO  = 2.0
    MIN_RADIUS = 1


def surface_style() -> ContainerStyle:
    return ContainerStyle(RectStyle(Palette.SURFACE))

def overlay_style() -> ContainerStyle:
    return ContainerStyle(RectStyle(Palette.OVERLAY, radius=Spacing.OVERLAY_RADIUS))

def top_bar_text_style() -> LabelStyle:
    return LabelStyle(Palette.DIM, TextPreset.HEADING, Palette.BACKGROUND)

def menu_background_style() -> ContainerStyle:
    return ContainerStyle(RectStyle(Palette.BACKGROUND))

def transparent_container_style() -> ContainerStyle:
    return ContainerStyle(background=None)

def content_text_style() -> LabelStyle:
    return LabelStyle(Palette.TEXT_PRIMARY, TextPreset.BODY, Palette.BACKGROUND, TextAlignment.CENTER)

def hero_value_style(color: Color = Palette.TEXT_PRIMARY) -> LabelStyle:
    return LabelStyle(color, TextPreset.DISPLAY, Palette.BACKGROUND, TextAlignment.LEFT)

def value_style(color: Color = Palette.TEXT_PRIMARY) -> LabelStyle:
    return LabelStyle(color, TextPreset.VALUE, Palette.BACKGROUND, TextAlignment.LEFT)

def caption_style() -> LabelStyle:
    return LabelStyle(Palette.DIM, TextPreset.SUBHEAD, Palette.BACKGROUND, TextAlignment.LEFT)

def weather_icon_layers(condition: WeatherCondition) -> list[IconLayer]:
    return WEATHER_ICONS.get(condition, WEATHER_ICONS[WeatherCondition.CLOUDY])

def weather_label(condition: WeatherCondition) -> str:
    return WEATHER_LABELS.get(condition, "--")

def band_for(value: float, bands: list[Band]) -> Band:
    for band in reversed(bands):
        if value >= band.lower:
            return band
    return DEFAULT_BAND
