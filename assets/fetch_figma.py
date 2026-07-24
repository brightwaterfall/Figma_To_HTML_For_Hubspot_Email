"""Fresh Figma -> HubSpot email asset + structure extract."""
import json
import sys
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
for p in (ASSETS, IMAGES, ICONS, ROOT / "css", ROOT / "fonts"):
    p.mkdir(parents=True, exist_ok=True)

# Left-to-right frame order
FRAMES = [
    ("email-01", "2259:309"),
    ("email-02", "2296:463"),
    ("email-03", "2016:274"),
    ("email-04", "2011:102"),
    ("email-05", "2223:189"),
]


def api(path):
    req = urllib.request.Request(
        f"https://api.figma.com/v1{path}",
        headers={"X-Figma-Token": TOKEN},
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode("utf-8"))


def walk(n, acc=None):
    if acc is None:
        acc = []
    acc.append(n)
    for c in n.get("children") or []:
        walk(c, acc)
    return acc


def has_image(n):
    return any(
        f.get("type") == "IMAGE" and f.get("visible", True) is not False
        for f in (n.get("fills") or [])
    )


def rgba(fill):
    if not fill or fill.get("type") != "SOLID":
        return None
    c = fill["color"]
    a = fill.get("opacity", 1) * c.get("a", 1)
    if a >= 0.999:
        return f"#{int(c['r']*255):02X}{int(c['g']*255):02X}{int(c['b']*255):02X}"
    return f"rgba({int(c['r']*255)},{int(c['g']*255)},{int(c['b']*255)},{a:.3f})"


print("Fetching nodes...")
ids = ",".join(fid for _, fid in FRAMES)
data = api(f"/files/{FILE}/nodes?ids={urllib.parse.quote(ids)}")
(ASSETS / "figma-nodes.json").write_text(json.dumps(data), encoding="utf-8")

# Export full frame PNGs @2x for QA
print("Exporting frame previews...")
frame_ids = ",".join(fid for _, fid in FRAMES)
imgs = api(f"/images/{FILE}?ids={urllib.parse.quote(frame_ids)}&format=png&scale=2")
for key, fid in FRAMES:
    url = (imgs.get("images") or {}).get(fid)
    if url:
        dest = IMAGES / f"{key}-figma.png"
        urllib.request.urlretrieve(url, dest)
        print("frame", dest.name, dest.stat().st_size)

# Collect export targets
exports = {}  # filename -> node_id


def add(fname, nid):
    if fname not in exports and nid:
        exports[fname] = nid


for key, fid in FRAMES:
    doc = data["nodes"][fid]["document"]
    nodes = walk(doc)

    for n in nodes:
        name = n.get("name", "")
        t = n.get("type")
        bb = n.get("absoluteBoundingBox") or {}
        w, h = bb.get("width") or 0, bb.get("height") or 0
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

    # Hero: largest image-fill rect ~600 wide
    heroes = [
        n
        for n in nodes
        if has_image(n)
        and (n.get("absoluteBoundingBox") or {}).get("width", 0) >= 500
    ]
    heroes.sort(
        key=lambda n: (n.get("absoluteBoundingBox") or {}).get("width", 0)
        * (n.get("absoluteBoundingBox") or {}).get("height", 0),
        reverse=True,
    )
    if heroes:
        add(f"{key}-hero.png", heroes[0]["id"])

    # Card / medium images
    mediums = [
        n
        for n in nodes
        if (n.get("name", "").startswith("ðŸ“·") or n.get("type") == "FRAME")
        and "Image" in n.get("name", "")
        and 150
        <= (n.get("absoluteBoundingBox") or {}).get("width", 0)
        <= 350
    ]
    for i, n in enumerate(mediums[:4]):
        add(f"{key}-card-{i+1}.png", n["id"])

    # Emoji / deco
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

    # Avatar ellipses
    ellipses = [
        n
        for n in nodes
        if n.get("type") == "ELLIPSE"
        and 30 <= (n.get("absoluteBoundingBox") or {}).get("width", 0) <= 50
    ]
    if ellipses:
        add(f"{key}-avatar.png", ellipses[0]["id"])

# Text extract
text = {}
structure = {}
for key, fid in FRAMES:
    doc = data["nodes"][fid]["document"]
    nodes = walk(doc)
    bb = doc.get("absoluteBoundingBox") or {}
    fills = doc.get("fills") or []
    structure[key] = {
        "id": fid,
        "width": bb.get("width"),
        "height": bb.get("height"),
        "bg": rgba(fills[0]) if fills else None,
        "sections": [],
    }
    texts = []
    for n in nodes:
        if n.get("type") == "TEXT" and n.get("characters"):
            st = n.get("style") or {}
            fills_n = n.get("fills") or []
            texts.append(
                {
                    "name": n.get("name"),
                    "chars": n.get("characters"),
                    "font": st.get("fontFamily"),
                    "weight": st.get("fontWeight"),
                    "size": st.get("fontSize"),
                    "lh": st.get("lineHeightPx"),
                    "ls": st.get("letterSpacing"),
                    "align": st.get("textAlignHorizontal"),
                    "color": rgba(fills_n[0]) if fills_n else None,
                    "w": (n.get("absoluteBoundingBox") or {}).get("width"),
                    "h": (n.get("absoluteBoundingBox") or {}).get("height"),
                }
            )
        # top-level rows
        if n.get("id") != doc.get("id") and n in (doc.get("children") or []):
            nf = n.get("fills") or []
            structure[key]["sections"].append(
                {
                    "name": n.get("name"),
                    "type": n.get("type"),
                    "w": (n.get("absoluteBoundingBox") or {}).get("width"),
                    "h": (n.get("absoluteBoundingBox") or {}).get("height"),
                    "bg": rgba(nf[0]) if nf else None,
                    "pt": n.get("paddingTop"),
                    "pr": n.get("paddingRight"),
                    "pb": n.get("paddingBottom"),
                    "pl": n.get("paddingLeft"),
                    "gap": n.get("itemSpacing"),
                    "cr": n.get("cornerRadius"),
                }
            )
    text[key] = texts

(ASSETS / "text-extract.json").write_text(
    json.dumps(text, indent=2, ensure_ascii=False), encoding="utf-8"
)
(ASSETS / "structure.json").write_text(
    json.dumps(structure, indent=2, ensure_ascii=False), encoding="utf-8"
)
(ASSETS / "export-map.json").write_text(
    json.dumps(exports, indent=2, ensure_ascii=False), encoding="utf-8"
)

print(f"Exporting {len(exports)} assets...")
ids = list(exports.values())
id_to_url = {}
for i in range(0, len(ids), 35):
    batch = ids[i : i + 35]
    q = ",".join(batch)
    payload = api(f"/images/{FILE}?ids={urllib.parse.quote(q)}&format=png&scale=2")
    id_to_url.update(payload.get("images") or {})
    print(f"  batch {i//35+1}: {len(payload.get('images') or {})}")

manifest = {}
for fname, nid in exports.items():
    url = id_to_url.get(nid)
    if not url:
        print("MISSING", fname, nid)
        continue
    folder = ICONS if fname.startswith("icon-") else IMAGES
    dest = folder / fname
    urllib.request.urlretrieve(url, dest)
    # knockout near-black bg for icons/logo/emoji
    if fname.startswith("icon-") or "logo" in fname or any(
        x in fname
        for x in (
            "smile",
            "handshake",
            "confetti",
            "launch",
            "laptop",
            "school",
            "backpack",
            "people",
        )
    ):
        try:
            from PIL import Image

            im = Image.open(dest).convert("RGBA")
            px = im.load()
            w, h = im.size
            for y in range(h):
                for x in range(w):
                    r, g, b, a = px[x, y]
                    if r <= 18 and g <= 18 and b <= 18:
                        px[x, y] = (0, 0, 0, 0)
            im.save(dest)
        except Exception as e:
            print("knockout skip", fname, e)
    manifest[fname] = str(dest.relative_to(ROOT)).replace("\\", "/")
    print("OK", fname, dest.stat().st_size)

(ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("DONE", len(manifest), "assets")
for key, s in structure.items():
    print(key, s["width"], s["height"], "sections", len(s["sections"]), "texts", len(text[key]))
