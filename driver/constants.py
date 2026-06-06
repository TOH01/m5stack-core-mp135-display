from pathlib import Path

INPUT_DEVICE_PATH = Path("/dev/input/event0")

FRAMEBUFFER_GRAPHICS_PATH = Path("/sys/class/graphics/fb1/")
FRAMEBUFFER_PATH = Path("/dev/fb1")
BACKLIGHT_PATH = Path("/sys/class/backlight/axp2101_m5stack_bl")

DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
DISPLAY_DIMENSIONS_PATH = FRAMEBUFFER_GRAPHICS_PATH / "virtual_size"
 
BITS_PER_PIXEL = 16
BITS_PER_PIXEL_PATH = FRAMEBUFFER_GRAPHICS_PATH / "bits_per_pixel"

BRIGHTNESS_PATH = BACKLIGHT_PATH / "brightness"
