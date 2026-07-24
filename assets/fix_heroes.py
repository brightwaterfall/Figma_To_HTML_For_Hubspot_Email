"""Rebuild hero PNGs from Figma frame renders with scoop + radii baked in.

Emailify overlap (email-01/03/05):
- Frame-local image at y≈105, h=380 (starts 34px above Full Image row)
- Top radii 24; title row radii [42,0,0,0] cream #FFFFF9 → bottom-left scoop
- Feedback badge ("Ton avis") baked into photo
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(r"E:\Freelancer project\figma_to_html")
IMAGES = ROOT / "images"
SCALE = 2
WHITE = (255, 255, 255, 255)


def load(n: int) -> Image.Image:
    return Image.open(IMAGES / f"email-{n:02d}-figma.png").convert("RGBA")


def crop_xywh(im: Image.Image, x: float, y: float, w: float, h: float) -> Image.Image:
    return im.crop(
        (
            int(x * SCALE),
            int(y * SCALE),
            int((x + w) * SCALE),
            int((y + h) * SCALE),
        )
    )


def ensure_top_radius(im: Image.Image, radius_design: float, fill=WHITE) -> Image.Image:
    """Reinforce Figma 24px top radii against white (logo) background."""
    w, h = im.size
    r = int(radius_design * SCALE)
    if r <= 0:
        return im
    mask = Image.new("L", (w, h), 255)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([0, 0, r, r], fill=0)
    draw.ellipse([0, 0, 2 * r, 2 * r], fill=255)
    draw.rectangle([w - r, 0, w, r], fill=0)
    draw.ellipse([w - 2 * r, 0, w, 2 * r], fill=255)
    rounded = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    rounded.paste(im, (0, 0), mask)
    bg = Image.new("RGBA", (w, h), fill)
    bg.paste(rounded, (0, 0), rounded)
    return bg


def build_hero(frame: Image.Image, image_y: float, image_h: float = 380, top_r: float = 24):
    band = crop_xywh(frame, 0, image_y, 600, image_h)
    return ensure_top_radius(band, top_r, fill=WHITE)


# Frame-local image tops from absoluteBoundingBox (image.y - frame.y)
HEROES = [
    (1, 105.5),  # 2743.5 - 2638
    (2, 102.5),  # nested Frame 7
    (3, 105.5),
    (5, 105.5),
]

for n, y in HEROES:
    out = build_hero(load(n), y, 380, 24)
    path = IMAGES / f"email-{n:02d}-hero.png"
    out.save(path, optimize=True)
    print(path.name, out.size, path.stat().st_size)

print("done")
