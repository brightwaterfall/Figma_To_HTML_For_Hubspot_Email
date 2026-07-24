"""Minimal asset export with long backoff + Pillow fallback icons."""
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

TOKEN = "YOUR_FIGMA_TOKEN"
FILE = "tUVlC3JZesnJMhvVqWrp4u"
ROOT = Path(r"E:\Freelancer project\figma_to_html")
ASSETS = ROOT / "assets"
IMAGES = ROOT / "images"
ICONS = ROOT / "icons"
IMAGES.mkdir(exist_ok=True)
ICONS.mkdir(exist_ok=True)

exports = json.loads((ASSETS / "export-map.json").read_text(encoding="utf-8")) if (ASSETS / "export-map.json").exists() else {}

# Rebuild export map from nodes if missing
if not exports:
    data = json.loads((ASSETS / "figma-nodes.json").read_text(encoding="utf-8"))
    frames = [
        ("email-01", "2259:309"),
        ("email-02", "2296:463"),
        ("email-03", "2016:274"),
        ("email-04", "2011:102"),
        ("email-05", "2223:189"),
    ]

    def walk(n, a=None):
        if a is None:
            a = []
        a.append(n)
        for c in n.get("children") or []:
            walk(c, a)
        return a

    def has_image(n):
        return any(f.get("type") == "IMAGE" and f.get("visible", True) is not False for f in (n.get("fills") or []))

    def add(fname, nid):
        if fname not in exports and nid:
            exports[fname] = nid

    for key, fid in frames:
        nodes = walk(data["nodes"][fid]["document"])
        for n in nodes:
            name = n.get("name", "")
            nid = n.get("id")
            if "[LOGO]" in name or "EtrePROF-Violet" in name:
                add("logo-etreprof.png", nid)
            if "Scholavie" in name:
                add("logo-scholavie.png", nid)
            if name == "Instagram (SVG Icon)":
                add("icon-instagram.png", nid)
            if name == "Facebook (SVG Icon)":
                add("icon-facebook.png", nid)
            if name == "X (SVG Icon)":
                add("icon-x.png", nid)
            if name == "YouTube (SVG Icon)":
                add("icon-youtube.png", nid)
        heroes = [n for n in nodes if has_image(n) and (n.get("absoluteBoundingBox") or {}).get("width", 0) >= 500]
        heroes.sort(key=lambda n: (n.get("absoluteBoundingBox") or {}).get("width", 0) * (n.get("absoluteBoundingBox") or {}).get("height", 0), reverse=True)
        if heroes:
            add(f"{key}-hero.png", heroes[0]["id"])
        mediums = [n for n in nodes if "Image" in n.get("name", "") and 150 <= (n.get("absoluteBoundingBox") or {}).get("width", 0) <= 350]
        for i, n in enumerate(mediums[:4]):
            add(f"{key}-card-{i+1}.png", n["id"])
        for ename, suffix in [
            ("handshake", "handshake"),
            ("confetti", "confetti"),
            ("beaming face with smiling eyes", "smile"),
            ("launch", "launch"),
            ("Laptop computer with blank screen for remote work", "laptop"),
            ("school", "school"),
            ("school backpack", "backpack"),
            ("three men", "people"),
        ]:
            found = [n for n in nodes if n.get("name") == ename]
            if found:
                add(f"{key}-{suffix}.png", found[0]["id"])
        ellipses = [n for n in nodes if n.get("type") == "ELLIPSE" and 30 <= (n.get("absoluteBoundingBox") or {}).get("width", 0) <= 50]
        if ellipses:
            add(f"{key}-avatar.png", ellipses[0]["id"])
    (ASSETS / "export-map.json").write_text(json.dumps(exports, indent=2), encoding="utf-8")

print("exports", len(exports))


def api_images(ids, retries=8):
    q = ",".join(ids)
    url = f"https://api.figma.com/v1/images/{FILE}?ids={urllib.parse.quote(q)}&format=png&scale=2"
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"X-Figma-Token": TOKEN})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 60 * (attempt + 1)
                print(f"429 wait {wait}s (attempt {attempt+1})", flush=True)
                time.sleep(wait)
                continue
            raise
    return {"images": {}}


# Priority assets first
priority = [
    "logo-etreprof.png",
    "logo-scholavie.png",
    "icon-instagram.png",
    "icon-facebook.png",
    "icon-x.png",
    "icon-youtube.png",
    "email-01-hero.png",
    "email-02-hero.png",
    "email-03-hero.png",
    "email-05-hero.png",
    "email-02-card-1.png",
    "email-02-card-2.png",
    "email-03-card-1.png",
    "email-02-avatar.png",
    "email-02-smile.png",
    "email-02-handshake.png",
    "email-02-confetti.png",
    "email-03-smile.png",
    "email-03-launch.png",
    "email-03-laptop.png",
    "email-05-smile.png",
    "email-05-handshake.png",
    "email-05-confetti.png",
    "email-05-school.png",
    "email-05-backpack.png",
    "email-05-people.png",
]
# Also full frames
frames = {
    "email-01-figma.png": "2259:309",
    "email-02-figma.png": "2296:463",
    "email-03-figma.png": "2016:274",
    "email-04-figma.png": "2011:102",
    "email-05-figma.png": "2223:189",
}

# Export frames
print("frames...", flush=True)
payload = api_images(list(frames.values()))
for fname, nid in frames.items():
    url = (payload.get("images") or {}).get(nid)
    if url:
        dest = IMAGES / fname
        urllib.request.urlretrieve(url, dest)
        print("OK", fname, dest.stat().st_size, flush=True)
time.sleep(5)

# Export priority in small batches
needed = [(f, exports[f]) for f in priority if f in exports]
print("needed", len(needed), flush=True)
id_to_url = {}
for i in range(0, len(needed), 10):
    batch = needed[i : i + 10]
    ids = [nid for _, nid in batch]
    payload = api_images(ids)
    id_to_url.update(payload.get("images") or {})
    print(f"batch {i//10+1}", len(payload.get("images") or {}), flush=True)
    time.sleep(5)

from PIL import Image

manifest = {}
for fname, nid in needed:
    url = id_to_url.get(nid)
    if not url:
        print("MISS", fname, flush=True)
        continue
    folder = ICONS if fname.startswith("icon-") else IMAGES
    dest = folder / fname
    urllib.request.urlretrieve(url, dest)
    if fname.startswith("icon-") or "logo" in fname or any(
        x in fname for x in ("smile", "handshake", "confetti", "launch", "laptop", "school", "backpack", "people")
    ):
        im = Image.open(dest).convert("RGBA")
        px = im.load()
        w, h = im.size
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if r <= 18 and g <= 18 and b <= 18:
                    px[x, y] = (0, 0, 0, 0)
        im.save(dest)
    manifest[fname] = str(dest.relative_to(ROOT)).replace("\\", "/")
    print("OK", fname, dest.stat().st_size, flush=True)

(ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("DONE", len(manifest), flush=True)
