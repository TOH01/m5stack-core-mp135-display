from pathlib import Path
from PIL import Image

ASSETS_DIR = Path(__file__).parent.parent / "assets"
_ICON_CACHE = {}

def get_tinted_icon(name: str, size: tuple[int, int], color: tuple[int, int, int] | None = None) -> Image.Image:
    """Loads, resizes (preserving aspect ratio with Lanczos), and optionally tints a PNG template icon."""
    cache_key = (name, size, color)
    if cache_key in _ICON_CACHE:
        return _ICON_CACHE[cache_key]
        
    tmpl_path = ASSETS_DIR / f"{name}.png"
    if not tmpl_path.exists():
        raise FileNotFoundError(f"Icon template not found: {tmpl_path}")
        
    img = Image.open(tmpl_path).convert("RGBA")
    
    # Crop to content bounding box to remove empty padding around SVG paths
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    
    # Calculate scale factor to preserve aspect ratio within target size
    orig_w, orig_h = img.size
    target_w, target_h = size
    
    scale = min(target_w / orig_w, target_h / orig_h)
    new_w = max(1, int(orig_w * scale))
    new_h = max(1, int(orig_h * scale))
    
    # Resize with high-quality downsampling
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Tint the image if a color is provided, using the new scaled size
    if color is not None:
        mask = img.split()[-1]
        color_img = Image.new("RGBA", (new_w, new_h), color + (255,))
        tinted = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
        tinted.paste(color_img, (0, 0), mask)
        output = tinted
    else:
        output = img
    
    _ICON_CACHE[cache_key] = output
    return output
