"""Extract font-family/size/weight/style/color from email HTML files."""
from pathlib import Path
import re

ROOT = Path(r"E:\Freelancer project\figma_to_html")

style_re = re.compile(
    r"font-family:([^;]+);[^>]{0,200}?font-size:(\d+)px;[^>]{0,120}?line-height:([\d.]+)px;[^>]{0,80}?font-weight:(\d+);(?:[^>]{0,40}?font-style:(italic);)?[^>]{0,80}?color:(#[0-9A-Fa-f]{3,8})",
    re.I,
)

# Also catch cases where order differs - simpler scan of style attrs
attr_re = re.compile(r'style="([^"]+)"')

for p in sorted(ROOT.glob("email-0*.html")):
    print(f"\n======== {p.name} ========")
    text = p.read_text(encoding="utf-8")
    seen = set()
    for m in attr_re.finditer(text):
        s = m.group(1)
        if "font-family" not in s or "font-size" not in s:
            continue
        fam = re.search(r"font-family:([^;]+)", s)
        size = re.search(r"font-size:([\d.]+)px", s)
        lh = re.search(r"line-height:([\d.]+)px", s)
        wt = re.search(r"font-weight:(\d+)", s)
        ital = "italic" if "font-style:italic" in s else ""
        color = re.search(r"color:(#[0-9A-Fa-f]+)", s)
        if not (fam and size):
            continue
        key = (
            fam.group(1).strip()[:40],
            size.group(1),
            wt.group(1) if wt else "?",
            ital,
            lh.group(1) if lh else "?",
            color.group(1) if color else "?",
        )
        if key in seen:
            continue
        seen.add(key)
        # get nearby text content
        end = m.end()
        snippet = re.sub(r"<[^>]+>", " ", text[end : end + 120])
        snippet = re.sub(r"\s+", " ", snippet).strip()[:60]
        print(f"{key[0]} {key[1]} w{key[2]} {key[3]} lh={key[4]} {key[5]} :: {snippet!r}")
