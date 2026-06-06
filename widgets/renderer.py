from driver.display import Display
from PIL import Image, ImageDraw, ImageFont
from structures.dataclasses import Rect, Point, RectStyle, TextStyle, CircleStyle, LineStyle
from structures.enums import TextPreset, TextAlignment

FONT_MAP = {
    TextPreset.HEADING: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13),
    TextPreset.BODY: ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11),
}

class Renderer:
    def __init__(self, display: Display) -> None:
        self.display = display
        self.canvas = Image.new("RGB", (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.canvas)
        self.dirty_regions: list[Rect] = []

    def draw_rect(self, rect: Rect, style: RectStyle) -> None:
        self.draw.rounded_rectangle(
            (rect.x, rect.y, rect.x + rect.w, rect.y + rect.h),
            radius=style.radius, fill=style.fill,
            outline=style.outline, width=style.outline_width
        )
        self.dirty_regions.append(rect)

    def draw_circle(self, center: Point, radius: int, style: CircleStyle) -> None:
        self.draw.ellipse(
            (center.x - radius, center.y - radius, center.x + radius, center.y + radius),
            fill=style.fill, outline=style.outline, width=style.outline_width
        )
        self.dirty_regions.append(Rect(center.x - radius, center.y - radius, radius * 2, radius * 2))

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
        bbox = font.getbbox(text)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        if text_w > rect.w or text_h > rect.h:
            raise ValueError(f"Text '{text}' ({text_w}x{text_h}) exceeds rect ({rect.w}x{rect.h})")

        if style.alignment == TextAlignment.LEFT:
            x = rect.x
        elif style.alignment == TextAlignment.CENTER:
            x = rect.x + (rect.w - text_w) // 2
        else:
            x = rect.x + rect.w - text_w

        y = rect.y + (rect.h - text_h) // 2

        self.draw.text((x, y), text, fill=style.color, font=font)
        self.dirty_regions.append(rect)

    def update(self) -> None:
        for rect in self.dirty_regions:
            region = self.canvas.crop((rect.x, rect.y, rect.x + rect.w, rect.y + rect.h))
            raw = region.tobytes()
            buf = bytearray()
            for i in range(0, len(raw), 3):
                r, g, b = raw[i], raw[i + 1], raw[i + 2]
                buf += ((r & 0xF8) << 8 | (g & 0xFC) << 3 | (b >> 3)).to_bytes(2, "little")
            self.display.draw_region(rect.x, rect.y, rect.w, rect.h, buf)
        self.dirty_regions.clear()