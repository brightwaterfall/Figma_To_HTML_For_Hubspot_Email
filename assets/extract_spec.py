import json
from pathlib import Path

p = Path(r"E:\Freelancer project\figma_to_html\assets\figma-nodes.json")
data = json.loads(p.read_text(encoding="utf-8"))
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


out = []
for key, fid in frames:
    doc = data["nodes"][fid]["document"]
    bb = doc["absoluteBoundingBox"]
    out.append(f"==== {key} {int(bb['width'])}x{int(bb['height'])} ====")
    for ch in doc.get("children") or []:
        fills = ch.get("fills") or []
        bg = ""
        if fills and fills[0].get("type") == "SOLID":
            c = fills[0]["color"]
            bg = f" #{int(c['r']*255):02X}{int(c['g']*255):02X}{int(c['b']*255):02X}"
        h = int((ch.get("absoluteBoundingBox") or {}).get("height") or 0)
        out.append(
            f"  SECTION: {ch.get('name')} h={h} pt={ch.get('paddingTop')} pr={ch.get('paddingRight')} pb={ch.get('paddingBottom')} pl={ch.get('paddingLeft')}{bg}"
        )
    for n in walk(doc):
        if n.get("type") == "TEXT" and n.get("characters"):
            st = n.get("style") or {}
            fills = n.get("fills") or []
            col = ""
            if fills and fills[0].get("type") == "SOLID":
                c = fills[0]["color"]
                col = f"#{int(c['r']*255):02X}{int(c['g']*255):02X}{int(c['b']*255):02X}"
            chars = n["characters"].replace("\n", " / ")
            out.append(
                f"  TEXT {st.get('fontSize')}px {st.get('fontFamily')} w{st.get('fontWeight')} {st.get('textAlignHorizontal')} {col}: {chars[:160]}"
            )
        if n.get("type") == "FRAME" and "Button" in n.get("name", ""):
            fills = n.get("fills") or []
            bg = ""
            if fills and fills[0].get("type") == "SOLID":
                c = fills[0]["color"]
                bg = f"#{int(c['r']*255):02X}{int(c['g']*255):02X}{int(c['b']*255):02X}"
            bb2 = n.get("absoluteBoundingBox") or {}
            out.append(
                f"  BTN bg={bg} pad={n.get('paddingTop')}/{n.get('paddingRight')}/{n.get('paddingBottom')}/{n.get('paddingLeft')} cr={n.get('cornerRadius')} {int(bb2.get('width') or 0)}x{int(bb2.get('height') or 0)}"
            )

Path(r"E:\Freelancer project\figma_to_html\assets\spec.txt").write_text(
    "\n".join(out), encoding="utf-8"
)
print("wrote", len(out), "lines")
