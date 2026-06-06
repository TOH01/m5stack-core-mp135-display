import math

def map_brightness(brightness: int) -> int:
    return (math.ceil(brightness / 2) + 50)
