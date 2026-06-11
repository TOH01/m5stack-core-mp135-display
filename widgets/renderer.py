import numpy as np
from PIL import Image, ImageDraw

import widgets.utils as utils
from driver.display import Display
from structures.dataclasses import CircleStyle, LineStyle, Point, Rect, RectStyle, TextStyle
from structures.enums import TextAlignment
from theme import FONT_MAP

CIRCLE_SUPERSAMPLE = 4


class Renderer:
    def __init__(self, display: Display) -> None:
        self.display = display
        self.canvas = Image.new("RGB", (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.canvas)
        self.dirty_regions: list[Rect] = []

    def draw_rect(self, rect: Rect, style: RectStyle) -> None:
        self.draw.rounded_rectangle(
            (rect.x, rect.y, rect.x + rect.w - 1, rect.y + rect.h - 1),
            radius=style.radius,
            fill=style.fill,
            outline=style.outline,
            width=style.outline_width,
        )
        self.dirty_regions.append(rect)

    def draw_circle(self, center: Point, radius: int, style: CircleStyle) -> None:
        ss = CIRCLE_SUPERSAMPLE
        d = radius * 2 + 1
        big = d * ss
        tile = Image.new("RGBA", (big, big), (0, 0, 0, 0))
        tile_draw = ImageDraw.Draw(tile)
        tile_draw.ellipse(
            (0, 0, big - 1, big - 1),
            fill=(*style.fill, 255) if style.fill is not None else None,
            outline=(*style.outline, 255) if style.outline else None,
            width=style.outline_width * ss,
        )

        tile = tile.resize((d, d), Image.LANCZOS)

        pos = (center.x - radius, center.y - radius)
        self.canvas.paste(tile, pos, tile)

        self.dirty_regions.append(Rect(center.x - radius, center.y - radius, d, d))

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
        
        if style.tracking > 0:
            text_w = sum(font.getlength(c) for c in text) + (len(text) - 1) * style.tracking
            bbox = font.getbbox(text)
            text_h = bbox[3] - bbox[1] if bbox else 0
        else:
            bbox = font.getbbox(text)
            text_w = bbox[2] - bbox[0] if bbox else 0
            text_h = bbox[3] - bbox[1] if bbox else 0

        if text_w > rect.w:
            while text:
                curr_w = (
                    (sum(font.getlength(c) for c in text + "…") + len(text) * style.tracking)
                    if style.tracking > 0
                    else font.getbbox(text + "…")[2]
                )
                if curr_w <= rect.w:
                    break
                text = text[:-1]
            text += "…"
            if style.tracking > 0:
                text_w = sum(font.getlength(c) for c in text) + (len(text) - 1) * style.tracking
                bbox = font.getbbox(text)
                text_h = bbox[3] - bbox[1] if bbox else 0
            else:
                bbox = font.getbbox(text)
                text_w = bbox[2] - bbox[0] if bbox else 0
                text_h = bbox[3] - bbox[1] if bbox else 0

        if style.alignment == TextAlignment.LEFT:
            x = rect.x
        elif style.alignment == TextAlignment.CENTER:
            x = rect.x + (rect.w - text_w) // 2
        else:
            x = rect.x + rect.w - text_w

        top_offset = bbox[1] if bbox else 0
        y = rect.y + (rect.h - text_h) // 2 - top_offset

        if style.tracking > 0:
            curr_x = x
            for c in text:
                self.draw.text((curr_x, y), c, fill=style.color, font=font)
                curr_x += font.getlength(c) + style.tracking
        else:
            self.draw.text((x, y), text, fill=style.color, font=font)
        self.dirty_regions.append(rect)

    def update(self) -> None:
        for rect in utils.merge_regions(self.dirty_regions):
            region = self.canvas.crop((rect.x, rect.y, rect.x + rect.w, rect.y + rect.h))
            arr = np.asarray(region, dtype=np.uint16)
            rgb565 = ((arr[..., 0] & 0xF8) << 8) | ((arr[..., 1] & 0xFC) << 3) | (arr[..., 2] >> 3)
            self.display.draw_region(rect, rgb565.astype("<u2").tobytes())
        self.dirty_regions.clear()
