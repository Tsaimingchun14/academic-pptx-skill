"""Render rough.js illustrations and export them for native-shape rebuilding.

Usage:  python3 render_illustrations.py ILLUS_JS OUT_DIR [name ...]
  ILLUS_JS  your file defining `const ILLUS = { name: { w, h, draw() {...} } }`
  OUT_DIR   receives <name>.png (preview / contact sheet), <name>.json (element export)
            and sizes.json (merged, so re-rendering a subset keeps the others)
Requires: npm install roughjs (in the work dir or OUT_DIR's parent), Playwright,
          Solitreo and Open Sans in ~/.fonts.
"""
import glob, json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
illus, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
names = sys.argv[3:]
os.makedirs(out, exist_ok=True)

def find_rough():
    for base in (os.getcwd(), os.path.dirname(illus), os.path.dirname(out)):
        p = os.path.join(base, "node_modules/roughjs/bundled/rough.js")
        if os.path.exists(p):
            return p
    sys.exit("rough.js not found: run `npm install roughjs` in the work dir")

def font(pattern):
    hits = sorted(glob.glob(os.path.expanduser(f"~/.fonts/{pattern}")))
    if not hits:
        sys.exit(f"font missing in ~/.fonts: {pattern}")
    return hits[0]

page = os.path.join(out, "_page.html")
open(page, "w").write(f"""<!doctype html><html><head><meta charset="utf-8">
<style>
@font-face {{ font-family: Solitreo; src: url(file://{font('Solitreo*.ttf')}); }}
@font-face {{ font-family: 'Open Sans'; src: url(file://{font('OpenSans*Regular*.ttf')}); }}
body {{ margin:0; background: transparent; }} svg {{ display:block; }}
</style>
<script src="file://{find_rough()}"></script>
<script src="file://{HERE}/draw_helpers.js"></script>
<script src="file://{illus}"></script></head><body></body></html>""")

EXPORT = """() => {
  const out = [];
  SVG.querySelectorAll('path,circle,text').forEach(el => {
    const A = k => el.getAttribute(k);
    if (el.tagName === 'path') out.push({ t: 'path', d: A('d'), stroke: A('stroke'), sw: +(A('stroke-width') || 0),
        fill: A('fill'), dash: A('stroke-dasharray'), role: A('data-role') });
    else if (el.tagName === 'circle') out.push({ t: 'dot', cx: +A('cx'), cy: +A('cy'), r: +A('r'), fill: A('fill') });
    else {
      const b = el.getBBox(), runs = [];
      el.childNodes.forEach(c => runs.push({ s: c.textContent, sub: c.nodeType === 1 }));
      out.push({ t: 'text', x: b.x, y: b.y, w: b.width, h: b.height, runs, size: +A('font-size'),
                 color: A('fill'), anchor: A('text-anchor'), bold: A('font-weight') === 'bold' });
    }
  });
  return out; }"""

sizes_path = os.path.join(out, "sizes.json")
sizes = json.load(open(sizes_path)) if os.path.exists(sizes_path) else {}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(device_scale_factor=3)
    pg.goto(f"file://{page}")
    pg.evaluate("Promise.all([document.fonts.load('22px Solitreo'), document.fonts.load('22px \"Open Sans\"')])")
    names = names or pg.evaluate("Object.keys(ILLUS)")
    for n in names:
        w, h = pg.evaluate("""(n) => {
          document.body.innerHTML = '';
          const I = ILLUS[n];
          SVG = document.createElementNS(NS, 'svg');
          SVG.setAttribute('width', I.w); SVG.setAttribute('height', I.h);
          document.body.appendChild(SVG); RC = rough.svg(SVG); SEED = 1; I.draw();
          return [I.w, I.h]; }""", n)
        pg.wait_for_timeout(50)
        pg.locator("svg").screenshot(path=os.path.join(out, f"{n}.png"), omit_background=True)
        json.dump(pg.evaluate(EXPORT), open(os.path.join(out, f"{n}.json"), "w"))
        sizes[n] = [w, h]
    b.close()
json.dump(sizes, open(sizes_path, "w"))
print("rendered:", ", ".join(names))
