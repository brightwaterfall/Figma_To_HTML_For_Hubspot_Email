"""Dump all unique text styles from Figma email frames vs HTML usage."""
from pathlib import Path
import json
import re
from collections import defaultdict

ROOT = Path(r"E:\Freelancer project\figma_to_html")
data = json.loads((ROOT / "assets" / "figma-nodes.json").read_text(encoding="utf-8"))

FRAMES = {
    "E01": "2259:309",
    "E02": "2296:463",
    "E03": "2016:274",
    "E04": "2011:102",
    "E05": "2223:189",
}


def hex_color(fills):
    if not fills or fills[0].get("type") != "SOLID":
        return None
    c = fills[0]["color"]
    o = fills[0].get("opacity", 1)
    r, g, b = int(c["r"] * 255), int(c["g"] * 255), int(c["b"] * 255)
    return f"#{r:02X}{g:02X}{b:02X}" + (f"@{o:.2f}" if o < 0.99 else "")


def walk(n, email, rows):
    if n.get("type") == "TEXT":
        style = n.get("style") or {}
        chars = (n.get("characters") or "").replace("\n", " ").replace("\u2028", " ")
        rows.append(
            {
                "email": email,
                "chars": chars[:70],
                "font": style.get("fontFamily"),
                "post": style.get("fontPostScriptName"),
                "size": style.get("fontSize"),
                "weight": style.get("fontWeight"),
                "italic": bool(style.get("italic")),
                "lh": style.get("lineHeightPx"),
                "lh%": style.get("lineHeightPercent"),
                "align": style.get("textAlignHorizontal"),
                "color": hex_color(n.get("fills")),
            }
        )
    for c in n.get("children") or []:
        walk(c, email, rows)


all_rows = []
for label, nid in FRAMES.items():
    walk(data["nodes"][nid]["document"], label, all_rows)

# Print per email
for label in FRAMES:
    print(f"\n======== {label} ========")
    for r in all_rows:
        if r["email"] != label:
            continue
        ital = " italic" if r["italic"] else ""
        print(
            f"{r['font']} {r['size']} w{r['weight']}{ital} lh={r['lh']:.1f} {r['align']} {r['color']}: {r['chars']!r}"
        )

# Unique font families / styles used
print("\n======== UNIQUE COMBOS ========")
combos = sorted(
    {
        (r["font"], r["size"], r["weight"], r["italic"], round(r["lh"] or 0, 1), r["color"])
        for r in all_rows
    }
)
for c in combos:
    print(c)
