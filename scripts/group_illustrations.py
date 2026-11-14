"""Group each illustration's native shapes ("ILL|<name>|...") into one named group
("Illustration: <name>") that can be moved as a unit or ungrouped for editing; round stroke
caps and joins for the hand-drawn look; give shapes readable names; add alt text to groups.

Usage: python3 group_illustrations.py deck.pptx [illustration_alts.json]
"""
import json, os, re, shutil, sys, zipfile
from lxml import etree

NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
P, A = "{%s}" % NS["p"], "{%s}" % NS["a"]
src = sys.argv[1]
alts_file = sys.argv[2] if len(sys.argv) > 2 else "illustration_alts.json"
alts = json.load(open(alts_file)) if os.path.exists(alts_file) else {}


def group_slide(data):
    root = etree.fromstring(data)
    tree = root.find(".//p:cSld/p:spTree", NS)
    nid = max(int(e.get("id")) for e in root.iter(P + "cNvPr")) + 1
    groups = {}
    for sp in list(tree):
        c = sp.find(".//p:cNvPr", NS)
        if c is None or not c.get("name", "").startswith("ILL|"):
            continue
        _, name, idx, role = c.get("name").split("|")
        groups.setdefault(name, []).append(sp)
        c.set("name", f"{name} {role} {idx}")
        ln = sp.find("p:spPr/a:ln", NS)
        if ln is not None and ln.find("a:noFill", NS) is None:
            ln.set("cap", "rnd")
            dash = ln.find("a:prstDash", NS)
            anchor = dash if dash is not None else ln.find("a:solidFill", NS)
            if anchor is not None:
                anchor.addnext(etree.Element(A + "round"))
    for name, sps in groups.items():
        boxes = []
        for sp in sps:
            x = sp.find("p:spPr/a:xfrm", NS)
            o, e = x.find("a:off", NS), x.find("a:ext", NS)
            ox, oy = int(o.get("x")), int(o.get("y"))
            boxes.append((ox, oy, ox + int(e.get("cx")), oy + int(e.get("cy"))))
        x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
        x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
        pos = tree.index(sps[0])
        g = etree.Element(P + "grpSp")
        nv = etree.SubElement(g, P + "nvGrpSpPr")
        etree.SubElement(nv, P + "cNvPr", id=str(nid), name=f"Illustration: {name}", descr=alts.get(name, ""))
        nid += 1
        etree.SubElement(nv, P + "cNvGrpSpPr")
        etree.SubElement(nv, P + "nvPr")
        xf = etree.SubElement(etree.SubElement(g, P + "grpSpPr"), A + "xfrm")
        for tagname, (vx, vy) in (("off", (x0, y0)), ("ext", (x1 - x0, y1 - y0)), ("chOff", (x0, y0)), ("chExt", (x1 - x0, y1 - y0))):
            attrs = {"x": str(vx), "y": str(vy)} if "Off" in tagname or tagname == "off" else {"cx": str(vx), "cy": str(vy)}
            etree.SubElement(xf, A + tagname, **attrs)
        for sp in sps:
            tree.remove(sp)
            g.append(sp)
        tree.insert(pos, g)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


tmp = src + ".tmp"
with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        if item.filename.endswith("/"):
            continue  # folder entries break cloud editors
        data = zin.read(item.filename)
        if re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
            data = group_slide(data)
        zout.writestr(item, data)
shutil.move(tmp, src)
print("grouped illustrations in", src)
