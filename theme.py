from pathlib import Path

from PIL import ImageFont

from structures.dataclasses import (
    CircleStyle,
    ContainerStyle,
    LabelStyle,
    RectStyle,
)
from structures.enums import TextPreset

BG: tuple[int, int, int] = (12, 15, 19)  # #0C0F13  full-screen fill
TEXT: tuple[int, int, int] = (233, 237, 242)  # #E9EDF2  values, names, active dot
SUB: tuple[int, int, int] = (138, 149, 163)  # #8A95A3  units, title, time, off names
FAINT: tuple[int, int, int] = (86, 97, 112)  # #566170  meta footers, inactive dots, off state
GOOD: tuple[int, int, int] = (91, 201, 138)  # #5BC98A  status dots, socket rings
WARN: tuple[int, int, int] = (224, 176, 92)  # #E0B05C  status dots, hot temp value
BAD: tuple[int, int, int] = (226, 104, 90)  # #E2685A  status dots only
SOCKET_ON_FILL: tuple[int, int, int] = (20, 35, 29)  # #14231D  socket on fill

FONT_DIR = Path(__file__).parent / "fonts"

_SEMIBOLD = str(FONT_DIR / "IBMPlexSans-SemiBold.ttf")
_MEDIUM = str(FONT_DIR / "IBMPlexSans-Medium.ttf")
_REGULAR = str(FONT_DIR / "IBMPlexSans-Regular.ttf")

FONT_MAP: dict[TextPreset, ImageFont.FreeTypeFont] = {
    TextPreset.HERO: ImageFont.truetype(_SEMIBOLD, 38),
    TextPreset.COLUMN_VALUE: ImageFont.truetype(_SEMIBOLD, 30),
    TextPreset.AIR_CELL_VALUE: ImageFont.truetype(_SEMIBOLD, 23),
    TextPreset.SOCKET_WATTS: ImageFont.truetype(_SEMIBOLD, 16),
    TextPreset.FOOTER_STAT: ImageFont.truetype(_SEMIBOLD, 12),
    TextPreset.HOUR_TEMP: ImageFont.truetype(_SEMIBOLD, 11),
    TextPreset.TIME: ImageFont.truetype(_MEDIUM, 12),
    TextPreset.SCREEN_TITLE: ImageFont.truetype(_SEMIBOLD, 11),
    TextPreset.UNIT: ImageFont.truetype(_MEDIUM, 10),
    TextPreset.MICRO_LABEL: ImageFont.truetype(_SEMIBOLD, 8),
    TextPreset.META_STATUS: ImageFont.truetype(_REGULAR, 8),
}

# ── Pre-built styles ──────────────────────────────────────────────
# Containers / panels
TRANSPARENT_CONTAINER = ContainerStyle()
BG_CONTAINER = ContainerStyle(RectStyle(fill=BG))

# Labels
LABEL_PRIMARY = LabelStyle(color=TEXT, preset=TextPreset.FOOTER_STAT)
LABEL_SUB = LabelStyle(color=SUB, preset=TextPreset.META_STATUS)
LABEL_TITLE = LabelStyle(color=SUB, preset=TextPreset.SCREEN_TITLE)
LABEL_TIME = LabelStyle(color=SUB, preset=TextPreset.TIME)

DOT_ACTIVE = CircleStyle(fill=TEXT)
DOT_INACTIVE = CircleStyle(fill=FAINT)
