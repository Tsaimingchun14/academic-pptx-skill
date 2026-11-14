// Rebuild an exported illustration (<dir>/<name>.json from render_illustrations.py) as native,
// editable PowerPoint shapes. Shapes are named "ILL|<name>|..." and grouped afterwards by
// group_illustrations.py.
//   const { addIllustration } = require("<skill>/scripts/vec.js");
//   addIllustration(pres, slide, "illus/doors.json", x, y, scale, "Front view of the cabinet ...");
//   ... after writeFile: python3 <skill>/scripts/group_illustrations.py deck.pptx
const fs = require("fs");
const path = require("path");
const PX = 0.01; // 100 px = 1 inch
const GREEK = /[Ͱ-Ͽἀ-῿]/;

function parseD(d) {
  const tok = d.match(/[MLCQZmlcqz]|-?\d*\.?\d+(?:e[-+]?\d+)?/g) || [];
  const cmds = []; let i = 0, cmd = null;
  const num = () => parseFloat(tok[i++]);
  while (i < tok.length) {
    if (/[A-Za-z]/.test(tok[i])) cmd = tok[i++].toUpperCase();
    if (cmd === "M") { cmds.push({ c: "M", p: [num(), num()] }); cmd = "L"; }
    else if (cmd === "L") cmds.push({ c: "L", p: [num(), num()] });
    else if (cmd === "C") cmds.push({ c: "C", p: [num(), num(), num(), num(), num(), num()] });
    else if (cmd === "Q") cmds.push({ c: "Q", p: [num(), num(), num(), num()] });
    else if (cmd === "Z") { cmds.push({ c: "Z", p: [] }); cmd = null; }
    else i++;
  }
  return cmds;
}
const hex = (c) => (c || "#000000").replace("#", "").toUpperCase();

// Split a label into runs: Latin in Solitreo, Greek in Open Sans (Solitreo has no Greek).
function labelRuns(runs) {
  const out = [];
  runs.filter(r => r.s.length).forEach(r => {
    let cur = "", greek = null;
    const flush = () => { if (cur) out.push({ text: cur, options: Object.assign({ fontFace: greek ? "Open Sans" : "Solitreo" }, r.sub ? { subscript: true } : {}) }); cur = ""; };
    for (const ch of r.s) { const g = GREEK.test(ch); if (greek !== null && g !== greek) flush(); greek = g; cur += ch; }
    flush();
  });
  return out;
}

const ALTS = {};
function addIllustration(pres, slide, jsonPath, x0, y0, scale = 1, alt = "") {
  const name = path.basename(jsonPath, ".json");
  if (alt) ALTS[name] = alt;
  const els = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
  const k = PX * scale;
  els.forEach((e, idx) => {
    const tag = `ILL|${name}|${idx}`;
    if (e.t === "path") {
      const cmds = parseD(e.d);
      const xs = [], ys = [];
      cmds.forEach(({ p }) => { for (let j = 0; j < p.length; j += 2) { xs.push(p[j]); ys.push(p[j + 1]); } });
      if (!xs.length) return;
      const minX = Math.min(...xs), minY = Math.min(...ys);
      const w = Math.max((Math.max(...xs) - minX) * k, 0.01), h = Math.max((Math.max(...ys) - minY) * k, 0.01);
      const X = (v) => (v - minX) * k, Y = (v) => (v - minY) * k;
      const pts = [];
      cmds.forEach(({ c, p }) => {
        if (c === "M") pts.push({ x: X(p[0]), y: Y(p[1]), moveTo: true });
        else if (c === "L") pts.push({ x: X(p[0]), y: Y(p[1]) });
        else if (c === "C") pts.push({ x: X(p[4]), y: Y(p[5]), curve: { type: "cubic", x1: X(p[0]), y1: Y(p[1]), x2: X(p[2]), y2: Y(p[3]) } });
        else if (c === "Q") pts.push({ x: X(p[2]), y: Y(p[3]), curve: { type: "quadratic", x1: X(p[0]), y1: Y(p[1]) } });
        else if (c === "Z") pts.push({ close: true });
      });
      const filled = e.fill && e.fill !== "none";
      const stroked = e.stroke && e.stroke !== "none" && e.sw > 0;
      const dash = e.dash ? (parseFloat(e.dash) <= 2 ? "sysDot" : "dash") : "solid";
      const role = e.role || (filled && !stroked ? "fill" : "stroke");
      slide.addShape(pres.ShapeType.custGeom, {
        x: x0 + minX * k, y: y0 + minY * k, w, h, points: pts,
        fill: filled ? { color: hex(e.fill) } : { type: "none" },
        line: stroked ? { color: hex(e.stroke), width: e.sw * 0.72 * scale, dashType: dash } : { type: "none" },
        objectName: `${tag}|${role}`,
      });
    } else if (e.t === "dot") {
      slide.addShape(pres.ShapeType.ellipse, {
        x: x0 + (e.cx - e.r) * k, y: y0 + (e.cy - e.r) * k, w: 2 * e.r * k, h: 2 * e.r * k,
        fill: { color: hex(e.fill) }, line: { type: "none" }, objectName: `${tag}|dot`,
      });
    } else if (e.t === "text") {
      const pad = e.w * 0.25 + 6; // slack so a substitute font still fits on one line
      const align = e.anchor === "middle" ? "center" : e.anchor === "end" ? "right" : "left";
      const bx = align === "center" ? e.x - pad / 2 : align === "right" ? e.x - pad : e.x;
      slide.addText(labelRuns(e.runs), {
        x: x0 + bx * k, y: y0 + e.y * k, w: (e.w + pad) * k, h: e.h * k,
        fontSize: e.size * 0.72 * scale, color: hex(e.color), bold: e.bold, align, valign: "middle",
        margin: 0, wrap: false, isTextBox: true, objectName: `${tag}|label`,
      });
    }
  });
}
// Call before running group_illustrations.py so groups get alt text.
function writeAlts(file = "illustration_alts.json") { fs.writeFileSync(file, JSON.stringify(ALTS)); }
module.exports = { addIllustration, writeAlts };
