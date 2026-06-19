from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import widgets.utils as utils
from driver.display import Display
from structures.dataclasses import CircleStyle, LineStyle, Point, Rect, RectStyle, TextStyle
from structures.enums import TextAlignment, TextPreset

FONT_DIR = Path(__file__).parent.parent / "fonts"

FONT_MAP = {
    TextPreset.HEADING: ImageFont.truetype(str(FONT_DIR / "DejaVuSans-Bold.ttf"), 14),
    TextPreset.BODY: ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 11),
    TextPreset.VALUE: ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 22),
    TextPreset.DISPLAY: ImageFont.truetype(str(FONT_DIR / "DejaVuSans-Bold.ttf"), 58),
    TextPreset.SUBHEAD: ImageFont.truetype(str(FONT_DIR / "DejaVuSans.ttf"), 16),
    TextPreset.ICON: ImageFont.truetype(str(FONT_DIR / "MaterialSymbolsRounded.ttf"), 28),
}

SUPERSAMPLE = 4
CIRCLE_SUPERSAMPLE = SUPERSAMPLE
PILL_SUPERSAMPLE = SUPERSAMPLE


class Renderer:
    def __init__(self, display: Display) -> None:
        self.display = display
        self.canvas = Image.new("RGB", (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.canvas)
        self.dirty_regions: list[Rect] = []

    def draw_rect(self, rect: Rect, style: RectStyle) -> None:
        self.draw.rounded_rectangle((rect.x, rect.y, rect.x + rect.w - 1, rect.y + rect.h - 1), radius=style.radius, fill=style.fill, outline=style.outline, width=style.outline_width)
        self.dirty_regions.append(rect)

    def draw_circle(self, center: Point, radius: int, style: CircleStyle) -> None:
        ss = CIRCLE_SUPERSAMPLE
        d = radius * 2 + 1
        big = d * ss
        tile = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        tile_draw = ImageDraw.Draw(tile)
        tile_draw.ellipse((0, 0, big - 1, big - 1), fill=(*style.fill, 255), outline=(*style.outline, 255) if style.outline else None, width=style.outline_width * ss)

        tile = tile.resize((d, d), Image.LANCZOS)

        pos = (center.x - radius, center.y - radius)
        self.canvas.paste(tile, pos, tile)

        self.dirty_regions.append(Rect(center.x - radius, center.y - radius, d, d))

    def draw_pill(self, rect: Rect, style: RectStyle) -> None:
        big_w, big_h = rect.w * PILL_SUPERSAMPLE, rect.h * PILL_SUPERSAMPLE
        tile = Image.new("RGBA", (big_w, big_h), (0, 0, 0, 0))
        tile_draw = ImageDraw.Draw(tile)
        tile_draw.rounded_rectangle((0, 0, big_w - 1, big_h - 1), radius=big_h // 2, fill=(*style.fill, 255), outline=(*style.outline, 255) if style.outline else None, width=style.outline_width * PILL_SUPERSAMPLE)

        tile = tile.resize((rect.w, rect.h), Image.LANCZOS)

        self.canvas.paste(tile, (rect.x, rect.y), tile)

        self.dirty_regions.append(rect)

    def draw_line(self, start: Point, end: Point, style: LineStyle) -> None:
        self.draw.line((start.x, start.y, end.x, end.y), fill=style.color, width=style.width)
        half_w = style.width // 2
        x = min(start.x, end.x) - half_w
        y = min(start.y, end.y) - half_w
        w = abs(end.x - start.x) + style.width
        h = abs(end.y - start.y) + style.width
        self.dirty_regions.append(Rect(x, y, w, h))

    def draw_text(self, rect: Rect, text: str, style: TextStyle) -> None:
        font = FONT_MAP[style.preset]
        text_w = font.getlength(text)

        if text_w > rect.w:
            while text and font.getlength(text + "…") > rect.w:
                text = text[:-1]
            text += "…"
            text_w = font.getlength(text)

        if style.alignment == TextAlignment.LEFT:
            x = rect.x
        elif style.alignment == TextAlignment.CENTER:
            x = rect.x + int((rect.w - text_w) // 2)
        else:
            x = rect.x + int(rect.w - text_w)

        ascent, descent = font.getmetrics()
        y = rect.y + (rect.h - (ascent + descent)) // 2

        self.draw.text((x, y), text, fill=style.color, font=font)
        self.dirty_regions.append(rect)

    def update(self) -> None:
        for rect in utils.merge_regions(self.dirty_regions):
            region = self.canvas.crop((rect.x, rect.y, rect.x + rect.w, rect.y + rect.h))
            arr = np.asarray(region, dtype=np.uint16)
            rgb565 = ((arr[..., 0] & 0xF8) << 8) | ((arr[..., 1] & 0xFC) << 3) | (arr[..., 2] >> 3)
            self.display.draw_region(rect, rgb565.astype("<u2").tobytes())
        self.dirty_regions.clear()
