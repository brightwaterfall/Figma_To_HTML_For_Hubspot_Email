"""Build structure/text from cached nodes; export images with retry."""
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
for p in (ASSETS, IMAGES, ICONS, ROOT / "css", ROOT / "fonts"):
    p.mkdir(parents=True, exist_ok=True)

FRAMES = [
    ("email-01", "2259:309"),
    ("email-02", "2296:463"),
    ("email-03", "2016:274"),
    ("email-04", "2011:102"),
    ("email-05", "2223:189"),
]

data = json.loads((ASSETS / "figma-nodes.json").read_text(encoding="utf-8"))


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


def api_get(path, retries=6):
    url = f"https://api.figma.com/v1{path}"
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"X-Figma-Token": TOKEN})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 45 * (attempt + 1)
                print(f"429 — waiting {wait}s...")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("rate limit persisted")


exports = {}


def add(fname, nid):
    if fname not in exports and nid:
        exports[fname] = nid


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
    for n in doc.get("children") or []:
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
    texts = []
    for n in nodes:
        name = n.get("name", "")
        nid = n.get("id")
        if n.get("type") == "TEXT" and n.get("characters"):
            st = n.get("style") or {}
            fills_n = n.get("fills") or []
            texts.append(
                {
                    "chars": n.get("characters"),
                    "font": st.get("fontFamily"),
                    "weight": st.get("fontWeight"),
                    "size": st.get("fontSize"),
                    "lh": st.get("lineHeightPx"),
                    "align": st.get("textAlignHorizontal"),
                    "color": rgba(fills_n[0]) if fills_n else None,
                }
            )
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

    mediums = [
        n
        for n in nodes
        if "Image" in n.get("name", "")
        and 150 <= (n.get("absoluteBoundingBox") or {}).get("width", 0) <= 350
    ]
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

    ellipses = [
        n
        for n in nodes
        if n.get("type") == "ELLIPSE"
        and 30 <= (n.get("absoluteBoundingBox") or {}).get("width", 0) <= 50
    ]
    if ellipses:
        add(f"{key}-avatar.png", ellipses[0]["id"])

    text[key] = texts

(ASSETS / "text-extract.json").write_text(json.dumps(text, indent=2, ensure_ascii=False), encoding="utf-8")
(ASSETS / "structure.json").write_text(json.dumps(structure, indent=2, ensure_ascii=False), encoding="utf-8")
(ASSETS / "export-map.json").write_text(json.dumps(exports, indent=2, ensure_ascii=False), encoding="utf-8")
print("structure/text ready")
for k, s in structure.items():
    print(k, int(s["width"]), int(s["height"]), len(s["sections"]), "sections,", len(text[k]), "texts")

# Frame previews first
print("Exporting frame previews...")
frame_ids = ",".join(fid for _, fid in FRAMES)
imgs = api_get(f"/images/{FILE}?ids={urllib.parse.quote(frame_ids)}&format=png&scale=2")
for key, fid in FRAMES:
    url = (imgs.get("images") or {}).get(fid)
    if url:
        dest = IMAGES / f"{key}-figma.png"
        urllib.request.urlretrieve(url, dest)
        print("frame", dest.name, dest.stat().st_size)

print(f"Exporting {len(exports)} assets...")
ids = list(exports.values())
id_to_url = {}
for i in range(0, len(ids), 25):
    batch = ids[i : i + 25]
    q = ",".join(batch)
    payload = api_get(f"/images/{FILE}?ids={urllib.parse.quote(q)}&format=png&scale=2")
    id_to_url.update(payload.get("images") or {})
    print(f"batch {i//25+1}: {len(payload.get('images') or {})}")
    time.sleep(3)

manifest = {}
for fname, nid in exports.items():
    url = id_to_url.get(nid)
    if not url:
        print("MISSING", fname)
        continue
    folder = ICONS if fname.startswith("icon-") else IMAGES
    dest = folder / fname
    urllib.request.urlretrieve(url, dest)
    if fname.startswith("icon-") or "logo" in fname or any(
        x in fname
        for x in ("smile", "handshake", "confetti", "launch", "laptop", "school", "backpack", "people")
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
            print("knockout", fname, e)
    manifest[fname] = str(dest.relative_to(ROOT)).replace("\\", "/")
    print("OK", fname, dest.stat().st_size)

(ASSETS / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print("DONE", len(manifest))
