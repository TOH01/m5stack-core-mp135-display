import mmap
from pathlib import Path

import driver.constants as constants
import driver.utils as utils
from structures.dataclasses import Rect


class Display:
    def __init__(self, framebuffer_path=constants.FRAMEBUFFER_PATH) -> None:
        self.width, self.height = self.get_dimensions()
        self.bpp = self.get_bits_per_pixel()
        self.framebuffer_path = framebuffer_path

        self.f = open(self.framebuffer_path, "r+b")
        self.size = self.width * self.height * (self.bpp // 8)
        self.framebuffer = mmap.mmap(self.f.fileno(), self.size, mmap.MAP_SHARED, mmap.PROT_WRITE)

    def _read_text(self, path: Path) -> str | None:
        try:
            return path.read_text().strip()
        except OSError:
            return None

    def _write_text(self, path: Path, content: str) -> None:
        try:
            path.write_text(content)
        except OSError:
            return None

    def get_dimensions(self) -> tuple[int, int]:
        raw = self._read_text(constants.DISPLAY_DIMENSIONS_PATH)

        if raw:
            try:
                w, h = raw.split(",")
                return int(w), int(h)
            except ValueError:
                pass

        return constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT

    def get_bits_per_pixel(self) -> int:
        raw = self._read_text(constants.BITS_PER_PIXEL_PATH)

        if raw:
            try:
                return int(raw)
            except ValueError:
                pass

        return constants.BITS_PER_PIXEL

    def get_brightness(self) -> int:
        raw = self._read_text(constants.BRIGHTNESS_PATH)

        if raw:
            try:
                return int(raw)
            except ValueError:
                pass

        return 0

    def set_brightness(self, brightness: int) -> None:
        # values below or at 50 will fully turn the backlight off
        actual_brightness = utils.map_brightness(brightness)
        if 50 <= actual_brightness <= 100:
            self._write_text(constants.BRIGHTNESS_PATH, str(actual_brightness))

    def close(self):
        self.framebuffer.close()
        self.f.close()

    def draw_region(self, rect: Rect, data: bytes) -> None:
        bytes_per_pixel = self.bpp // 8
        row_size = rect.w * bytes_per_pixel
        for row in range(rect.h):
            offset = ((rect.y + row) * self.width + rect.x) * bytes_per_pixel
            data_offset = row * row_size
            self.framebuffer[offset : offset + row_size] = data[
                data_offset : data_offset + row_size
            ]
