from driver.display import Display
from PIL import Image, ImageDraw

class Renderer:
    def __init__(self, display: Display) -> None:
        self.display = display
        self.canvas = Image.new("RGB", (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.canvas)

    def update(self):
        pass

    def draw_rect(self):
        pass


if data:
            img = draw_screen(data)
            buf = bytearray()
            # Convert RGB888 to RGB565 for framebuffer
            for r, g, b in img.getdata():
                buf += ((r & 0xF8) << 8 | (g & 0xFC) << 3 | (b >> 3)).to_bytes(2, "little")
            
            try:
                with open("/dev/fb1", "wb") as f:
                    f.write(buf)
            except OSError as e:
                print(f"Could not write to fb1: {e}")