from structures.dataclasses import Color, ContainerStyle, LabelStyle, RectStyle
from structures.enums import TextAlignment, TextPreset


class Palette:
    BACKGROUND   = Color(18, 18, 20)     # near-black
    SURFACE      = Color(30, 30, 35)     # dark gray
    OVERLAY      = Color(40, 40, 48)     # slate gray
    TEXT_PRIMARY = Color(240, 240, 240)  # off-white
    ACCENT       = Color(255, 255, 255)  # white
    MUTED        = Color(90, 90, 90)     # medium gray


class Spacing:
    SCREEN_W       = 320
    SCREEN_H       = 240
    BAR_HEIGHT     = 25
    PADDING        = 8
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
    return LabelStyle(Palette.TEXT_PRIMARY, TextPreset.HEADING, Palette.SURFACE)

def menu_background_style() -> ContainerStyle:
    return ContainerStyle(RectStyle(Palette.BACKGROUND))

def transparent_container_style() -> ContainerStyle:
    return ContainerStyle(background=None)

def content_text_style() -> LabelStyle:
    return LabelStyle(Palette.TEXT_PRIMARY, TextPreset.BODY, Palette.BACKGROUND, TextAlignment.CENTER)
