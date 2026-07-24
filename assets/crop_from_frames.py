"""Crop section assets from full-frame Figma PNG renders (@2x of 600px)."""
from pathlib import Path
from PIL import Image

ROOT = Path(r"E:\Freelancer project\figma_to_html")
IMAGES = ROOT / "images"
ICONS = ROOT / "icons"
IMAGES.mkdir(exist_ok=True)
ICONS.mkdir(exist_ok=True)
SCALE = 2


def open_frame(n):
    for name in (f"email-{n:02d}-figma.png", f"email-{n:02d}.png"):
        p = IMAGES / name
        if p.exists() and p.stat().st_size > 100000:
            return Image.open(p).convert("RGBA")
    raise FileNotFoundError(n)


def crop(im, x, y, w, h):
    return im.crop((int(x * SCALE), int(y * SCALE), int((x + w) * SCALE), int((y + h) * SCALE)))


def save(im, path):
    path = Path(path)
    im.save(path, optimize=True)
    print("saved", path.name, im.size, path.stat().st_size)


def knockout_white_bg(im, thresh=245):
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= thresh and g >= thresh and b >= thresh:
                px[x, y] = (255, 255, 255, 0)
    return im


# --- Email 01 ---
e1 = open_frame(1)
save(knockout_white_bg(crop(e1, 276, 29, 48, 51)), IMAGES / "logo-etreprof.png")
save(crop(e1, 0, 139, 600, 313), IMAGES / "email-01-hero.png")
# social icons in footer ~ y 1298+32
save(crop(e1, 228, 1330, 24, 24), ICONS / "icon-instagram.png")
save(crop(e1, 268, 1330, 24, 24), ICONS / "icon-facebook.png")
save(crop(e1, 308, 1332, 20, 20), ICONS / "icon-x.png")
save(crop(e1, 348, 1330, 24, 24), ICONS / "icon-youtube.png")

# --- Email 02 ---
e2 = open_frame(2)
save(crop(e2, 0, 136, 600, 313), IMAGES / "email-02-hero.png")
# resource thumbs approx relative y after logo+hero: ~449, then content
# From earlier: cards around relative y 826
save(crop(e2, 61, 826, 203, 108), IMAGES / "email-02-card-1.png")
save(crop(e2, 61, 963, 203, 108), IMAGES / "email-02-card-2.png")
save(crop(e2, 92, 1210, 38, 38), IMAGES / "email-02-avatar.png")
save(crop(e2, 248, 470, 35, 35), IMAGES / "email-02-confetti.png")
save(crop(e2, 283, 470, 35, 35), IMAGES / "email-02-handshake.png")
save(crop(e2, 318, 470, 35, 35), IMAGES / "email-02-smile.png")
save(crop(e2, 239, 1930, 119, 38), IMAGES / "logo-scholavie.png")

# --- Email 03 ---
e3 = open_frame(3)
save(crop(e3, 0, 139, 600, 313), IMAGES / "email-03-hero.png")
save(crop(e3, 80, 754, 203, 202), IMAGES / "email-03-card-1.png")
save(crop(e3, 248, 487, 35, 35), IMAGES / "email-03-smile.png")
save(crop(e3, 282, 486, 35, 37), IMAGES / "email-03-launch.png")
save(crop(e3, 317, 486, 35, 35), IMAGES / "email-03-laptop.png")

# --- Email 05 ---
e5 = open_frame(5)
save(crop(e5, 0, 139, 600, 313), IMAGES / "email-05-hero.png")
save(crop(e5, 248, 485, 35, 37), IMAGES / "email-05-smile.png")
save(crop(e5, 282, 485, 35, 37), IMAGES / "email-05-handshake.png")
save(crop(e5, 317, 485, 35, 37), IMAGES / "email-05-confetti.png")
# feature icons on right of lavender cards
save(crop(e5, 520, 900, 50, 50), IMAGES / "email-05-school.png")
save(crop(e5, 520, 1000, 50, 50), IMAGES / "email-05-backpack.png")
save(crop(e5, 520, 1100, 50, 50), IMAGES / "email-05-people.png")

print("crop complete")
