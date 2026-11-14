// Browser-side rough.js drawing helpers for the sketch style (100 px = 1 slide inch).
// Load after rough.js and before your own illustrations file, which must define
//   const ILLUS = { name: { w, h, draw() { ... } }, ... }
const INK = "#1E1E1E", BLUE = "#2F6FD8", BEIGE = "#E9D8C0", LBLUE = "#DCE5F5", LBEIGE = "#F3EADD";
const MUTED = "#737373", HIGHLIGHT = "#D9731A", PAPER = "#FAF9F6";
const NS = "http://www.w3.org/2000/svg";
let RC, SVG, SEED = 1;

function o(extra) { return Object.assign({ stroke: INK, strokeWidth: 2.4, roughness: 1, fillStyle: "solid", seed: SEED++ }, extra || {}); }
function add(n) { SVG.appendChild(n); return n; }
function tag(g, role) { g.querySelectorAll("path").forEach(p => p.setAttribute("data-role", role)); return g; }

// ---- basic shapes (beige/blue fills always keep an ink outline) ----
function rect(x, y, w, h, e) { return add(RC.rectangle(x, y, w, h, o(e))); }
function line(x1, y1, x2, y2, e) { return add(RC.line(x1, y1, x2, y2, o(e))); }
function ellipse(cx, cy, w, h, e) { return add(RC.ellipse(cx, cy, w, h, o(e))); }
function poly(pts, e) { return add(RC.polygon(pts, o(e))); }
function path(d, e) { return add(RC.path(d, o(e))); }
function arrow(x1, y1, x2, y2, e) {
  e = e || {};
  line(x1, y1, x2, y2, e);
  const a = Math.atan2(y2 - y1, x2 - x1), L = e.head || 14, s = 0.45;
  const he = Object.assign({}, e, { strokeLineDash: undefined });
  line(x2, y2, x2 - L * Math.cos(a - s), y2 - L * Math.sin(a - s), he);
  line(x2, y2, x2 - L * Math.cos(a + s), y2 - L * Math.sin(a + s), he);
}
// Small solid dots: plain SVG circles (rough filled ellipses turn hollow as shapes).
function dot(x, y, r, fill) {
  const c = document.createElementNS(NS, "circle");
  c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", r || 3.5); c.setAttribute("fill", fill || INK);
  return add(c);
}

// ---- highlight marks: orange, hand-drawn, dashed; use whatever form fits, as many as needed ----
const HL = { stroke: HIGHLIGHT, strokeWidth: 3, roughness: 1.4, bowing: 2, strokeLineDash: [10, 7], disableMultiStroke: true };
function hlLoop(cx, cy, w, h) { return tag(ellipse(cx, cy, w, h, HL), "highlight"); }
function hlUnderline(x1, y, x2) { return tag(line(x1, y, x2, y + 2, HL), "highlight"); }
function hlBox(x, y, w, h) { return tag(rect(x, y, w, h, Object.assign({ fill: "none" }, HL)), "highlight"); }
function hlArrow(x1, y1, x2, y2) {
  const g1 = tag(line(x1, y1, x2, y2, HL), "highlight");
  const a = Math.atan2(y2 - y1, x2 - x1), L = 14, s = 0.45, he = Object.assign({}, HL, { strokeLineDash: undefined });
  tag(line(x2, y2, x2 - L * Math.cos(a - s), y2 - L * Math.sin(a - s), he), "highlight");
  tag(line(x2, y2, x2 - L * Math.cos(a + s), y2 - L * Math.sin(a + s), he), "highlight");
  return g1;
}

// ---- labels: Solitreo; Greek falls back to Open Sans (same in the exported text boxes) ----
// Use <tspan baseline-shift="sub" font-size="70%"> for subscripts.
function text(x, y, s, e) {
  e = e || {};
  const t = document.createElementNS(NS, "text");
  t.setAttribute("x", x); t.setAttribute("y", y);
  t.setAttribute("font-family", "Solitreo, 'Open Sans', sans-serif");
  t.setAttribute("font-size", e.size || 22);           // 22 px ≈ 16 pt on the slide
  t.setAttribute("fill", e.color || INK);
  t.setAttribute("text-anchor", e.anchor || "start");
  if (e.bold) t.setAttribute("font-weight", "bold");
  t.innerHTML = s;
  return add(t);
}
function sub(base, s) { return `${base}<tspan baseline-shift="sub" font-size="70%">${s}</tspan>`; }
