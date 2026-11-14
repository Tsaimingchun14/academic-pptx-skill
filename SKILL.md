---
name: academic-pptx
description: "Use this skill whenever the user wants to create or improve a presentation for an academic context — conference papers, seminar talks, thesis defenses, grant briefings, lab meetings, invited lectures, or any presentation where the audience will evaluate reasoning and evidence. Triggers include: 'conference talk', 'seminar slides', 'thesis defense', 'research presentation', 'academic deck', 'academic presentation'. Also triggers when the user asks to 'make slides' in combination with academic content (e.g., 'make slides for my paper on X', 'create a presentation for my dissertation defense', 'build a deck for my grant proposal'). This skill governs CONTENT and STRUCTURE decisions. For the technical work of creating or editing the .pptx file itself, also read the pptx SKILL.md."
license: MIT (see LICENSE)
---

# Academic Presentations Skill

## How This Skill Works

This skill has two layers:

1. **This file** — governs content, argument structure, and design standards for academic presentations. Read it fully before planning any slides.
2. **PPTX skill** — governs the technical implementation (creating, editing, and QA-ing the .pptx file). Read it too.

**Always read both before writing any code or creating any files.**

---

## Quick Reference

| Task | Guide |
|------|-------|
| Content planning, argument structure, slide-by-slide rules | [content_guidelines.md](content_guidelines.md) |
| Per-slide-type patterns (title, methods, results, etc.) | [slide_patterns.md](slide_patterns.md) |
| Hand-drawn illustrations as editable shapes | [scripts/](scripts/) — `draw_helpers.js`, `render_illustrations.py`, `vec.js`, `group_illustrations.py` |
| Typeset equations | `scripts/render_equation.py` |
| Technical creation from scratch | PPTX skill → `pptxgenjs.md` |
| Technical editing of an existing file | PPTX skill → `editing.md` |

---

## Step 1: Identify Presentation Type

Before planning a single slide, determine which mode applies.

### Structured Argument (default for academic work)

Use for: conference papers, seminar talks, thesis defenses, dissertation chapters, grant briefings, internal lab presentations, policy briefings, consulting-style research deliverables.

**Priority order: argument structure → data → layout → aesthetics.**

Follow [content_guidelines.md](content_guidelines.md) in full.

### Visual / Narrative

Use for: public engagement talks, science communication to non-specialist audiences, funding pitches to lay panels, event keynotes.

Follow the PPTX skill's design-forward guidelines. Argument structure still matters, but visual storytelling and emotional engagement take priority.

### When in doubt

Default to **Structured Argument**. If the user mentions a paper, a study, a dataset, a thesis, a grant, or a conference, they almost certainly want structured argument mode.

---

## Step 2: Plan the Deck Before Creating Any Slides

Produce a slide-by-slide outline (title, action title, exhibit type) and confirm with the user if the deck is more than 10 slides or if the content is complex. Do not start building until the outline is agreed.

Use the ghost deck test during planning: read only the proposed action titles in sequence. They must tell the complete argument. If they don't, fix the outline before building.

---

## Step 3: Apply Design Standards

Academic presentations use **communication-first design**. These rules override the PPTX skill's design-forward defaults.

The visual style is a **hand-drawn sketchbook**: off-white paper, black ink, one blue for focus, beige fills, orange highlight marks, drawings made with rough.js. Use it on every slide, including title and conclusions (no dark slides). If the user supplies an institution template, ask how to combine it with this style before building.

### Color

| Role | Hex |
|------|-----|
| Background (paper) | `FAF9F6` |
| Ink: titles, outlines | `1E1E1E` |
| Body text | `2B2B2B` |
| Focus (what the slide is about) | `2F6FD8` (blue) |
| Fill for objects, bars | `E9D8C0` (beige) |
| Light fills | `DCE5F5` (light blue), `F3EADD` (light beige) |
| Highlight marks | `D9731A` (orange) |
| Muted text, citations | `737373` |

- **Blue marks the focus of the slide** — whatever the title is about: the key result, the group of interest, the step being explained, the passage under discussion. **Beige is everything around it** — context, comparison groups, background objects. Keep this mapping consistent across the deck.
- **Orange means "look here."** Draw it by hand, dashed, in whatever form suits the spot — a loop around a number, an underline, an arrow, a bracket, a box. Use as many as the content needs.
- Beige and light fills always keep an ink outline (they are too light to stand alone on the paper).
- Use color to **direct attention**, not for decoration. No gradients and no colors outside this palette.

### Typography

| Element | Size | Weight |
|---------|------|--------|
| Action title | 24–28 pt | Bold |
| Section header | 20–22 pt | Bold |
| Body bullets | 20 pt | Regular |
| Chart labels / annotations | 16–18 pt | Regular |
| Source citations on slides | 12–14 pt | Regular, muted color |

**Three typefaces, each with one job:**
- **Open Sans** for all slide text that is not part of a drawing: titles, captions, bullets, citations, tables. Set it as the deck's theme font (`pres.theme = { headFontFace: "Open Sans", bodyFontFace: "Open Sans" }`) so new text boxes inherit it.
- **Solitreo** (handwriting) for text inside drawings: labels, chart values, legends, annotations. Solitreo has no Greek, so Greek letters inside a label are written in Open Sans (the scripts do this automatically).
- **Neo Euler** for all mathematics (see Mathematical Expressions).

Use size and weight for hierarchy within each typeface. Solitreo has no bold weight; use synthesized bold.

### Layout

- Left-align all body text. Center only slide titles and axis labels.
- Consistent grid: all text boxes and figures align to the same margins (minimum 0.5" from slide edges).
- For result slides: figure on the left, interpretive bullets on the right. This matches natural left-to-right reading.
- White space is a signal of analytical clarity — do not fill every inch.
- 16:9 widescreen is the default. Confirm with the user if they know the venue's aspect ratio.
- **At most two focal areas per slide.** A focal area is one thing the eye goes to: a drawing, an equation block, a bullet group, a callout. Title and citation don't count. A row of comparable panels reads as one area. If a slide needs three (e.g. diagram + equation + bullets), or there is simply too much content, break it into two or more slides — never drop key information to make it fit.

### Drawings

Drawings are for visual aid and better understanding — they never replace key information. Every slide's key point stays fully on the slide.

- When complex information can be expressed as a drawing plus simpler words **without losing anything**, do it that way.
- Otherwise keep the key information on the slide as it is, and add a drawing beside it where it helps understanding.
- Speaker notes hold only what the presenter adds beyond the slide — never the key point or information the slide needs.
- If the key information and its drawing don't fit in two focal areas, break the content into two or more slides rather than cutting it.

Text in boxes is not a drawing: a diagram's nodes should be drawn things, not labeled rectangles.

Good moves:
- **Draw the setup or the thing being studied**: the experimental rig, the cell and its pathway, the field site on a map sketch, the classroom layout, the archive and its documents.
- **Show a concept by contrast**: before vs after, control vs treatment, the old model vs the new one, the expected pattern vs what was observed.
- **Turn a count into icons**: 12 participants = 12 small figures, 30 interviews = 30 speech bubbles, 5 sites = 5 pins; draw the subset that matters in blue.
- **Turn a comparison into bars and a key claim into a circled number**: two runtimes, two survey percentages, two effect sizes.
- **Turn a process into a path of drawn steps**: a sample through a lab protocol, a bill through parliament, a participant through a study.
- **Diagram nodes as drawn things**: a network as an hourglass, a population as a crowd of dots, a document as a page with lines, a process as a path with waypoints.
- **Conclusions**: a small drawing beside each takeaway.

**Charts are drawn by hand too** (rough.js bars, points, lines, with Solitreo labels and the values written on them). If the user provides a finished plot, insert it as given — cropped and enlarged enough to read, with its source cited — rather than redrawing it.

### Hand-drawn rendering (rough.js → editable shapes)

Every drawing is delivered as **native, editable shapes**, grouped per drawing — never as a picture. The user can move a group, ungroup it, recolor strokes, retype labels, and use Edit Points in PowerPoint (Google Slides keeps the shapes but has no Edit Points). The scripts live in `scripts/`:

1. Setup: `npm install roughjs` in the work dir; Playwright is usually preinstalled. Fonts into `~/.fonts`, then `fc-cache -f`:
   - Solitreo: `https://raw.githubusercontent.com/google/fonts/main/ofl/solitreo/Solitreo-Regular.ttf`
   - Open Sans (static, for rendering previews): `https://raw.githubusercontent.com/googlefonts/opensans/main/fonts/ttf/OpenSans-Regular.ttf` and `OpenSans-Bold.ttf`
2. Write your drawings in one file as `const ILLUS = { name: { w, h, draw() { ... } } }`, sized in **px at 100 px per inch of the drawing's slot on the slide** (22 px ≈ 16 pt). Use the helpers from `draw_helpers.js`: `rect`, `line`, `ellipse`, `poly`, `path`, `arrow`, `dot` (small solid dots — plain circles, since sketchy filled ones turn hollow as shapes), `text` and `sub()` for labels with subscripts, and the highlight marks `hlLoop`, `hlUnderline`, `hlArrow`, `hlBox`. Add small reusable glyphs for the talk's own subject (a person, a cell, a sensor, a document). Defaults: ink stroke ≈ 2.4 px, roughness ≈ 1, solid fills, a fixed seed per shape so re-renders are stable. Draw arrows as strokes, never as text glyphs.
3. Render and export: `python3 scripts/render_illustrations.py illus.js out/` → `out/<name>.png` (preview), `out/<name>.json` (shapes and labels), `out/sizes.json`.
4. Check a **contact sheet** of all PNGs on the paper color before building: label collisions are easiest to fix in the drawing code.
5. In the build script: `addIllustration(pres, slide, "out/<name>.json", x, y, scale, altText)` from `scripts/vec.js`, then `writeAlts()` before saving.
6. After `writeFile`: `python3 scripts/group_illustrations.py deck.pptx` — groups each drawing as "Illustration: <name>", rounds stroke ends, names the shapes, and adds alt text.
7. Text that belongs to the slide (titles, captions, takeaway sentences) stays native Open Sans text outside the drawing.
8. When delivering, tell the user to install Solitreo and Open Sans (in Google Slides: Font → More fonts) so labels show in the right font.

### Mathematical Expressions

Never type equations as plain text (`x_i^2`, `sigma^2`, `10^-6`). They look broken on screen. Always typeset them.

**Display equations → Neo Euler via XeLaTeX, inserted as transparent PNG.** Neo Euler is a complete OpenType math font in an upright, handwriting-inspired style, so every letter, Greek symbol, operator and fraction comes from one font.

1. Install Neo Euler: download `https://raw.githubusercontent.com/aliftype/euler-otf/master/euler.otf` into `~/.fonts`, run `fc-cache -f`. If it or xelatex cannot be installed, **stop and ask the user** — do not fall back to another math font silently.
2. Render each equation block with `python3 scripts/render_equation.py out/ name '<body>'`. The body goes inside `aligned`, e.g.
   ```latex
   \bar{x} &= \dfrac{1}{N}\sum_{i=1}^{N} x_i \\[10pt]
   \symbf{y} &= \symbf{A}\symbf{x} + \symbf{b}
   ```
   The script uses this preamble:
   ```latex
   \usepackage{amsmath,xcolor}
   \usepackage[math-style=upright,bold-style=upright]{unicode-math}
   \setmainfont{Neo Euler}[FakeBold=1.2]
   \setmathfont{Neo Euler}[FakeBold=1.2]
   ```
   - `math-style=upright` is required — Neo Euler has only upright letters, and Greek goes missing without it.
   - `FakeBold=1.2` thickens the strokes so the math holds up next to the ink drawings.
   - Use `\symbf{}` for bold vectors and matrices, `\dfrac` for display fractions, `\mathrm{}` for word subscripts, `aligned` with `\\[10pt]` spacing. Colors `focus`, `muted`, `highlight` are predefined for `\textcolor`.
3. Insert with `slide.addImage({ path, x, y, w, h, altText: "<equation in words>", objectName })`. Keep the PNG's aspect ratio; size it so the math is at least as large as 18–20 pt body text and fills its container without crowding.

**Symbols inside drawings** (e.g. x₁ or Δt next to an arrow) are Solitreo labels with `sub()` subscripts; Greek in them is set in Open Sans.

**Inline symbols in bullets and captions → native text runs, not images.** Use pptxgenjs `subscript: true` / `superscript: true` runs in Open Sans, e.g. `[{ text: "x", options: { italic: true } }, { text: "i", options: { subscript: true } }]`. Unicode Greek (σ, θ, μ) is fine inline.

### Avoid (Academic-Specific)

- **No decorative icons** — icons in colored circles, stock images, clip art are inappropriate for analytical academic presentations. Hand-drawn objects are welcome when they carry content.
- **No accent lines under titles** — use whitespace instead.
- **No color palettes beyond the one above** — unless the user supplies institution colors.
- **No full-bleed background images on content slides** — reserve for title/section dividers only if desired.
- **No text-heavy slides** — if the audience is reading, they are not listening. Maximum ~40 words of body text per content slide.

---

## Step 4: Build and QA

Follow the PPTX skill's QA procedure in full, including:
- Content QA via `markitdown`
- Visual QA via slide images (subagents if available)
- Fix-and-verify loop until a full pass reveals no new issues

**Additionally, run the academic-specific checks:**

```
Academic QA checklist:
□ Every content slide has an action title (complete sentence stating the takeaway)
□ Ghost deck test passes (action titles alone tell the full argument)
□ One exhibit per results slide; each exhibit has a "so what" annotation
□ Every borrowed figure or data point has an in-slide citation
□ A References slide exists at the end
□ Conclusions slide is the last non-appendix slide (not "Thank You" or a blank)
□ Contact information and/or QR code/link on the final slide
□ Font sizes are readable from the back of a room (≥ 20 pt body text)
□ No decorative elements that don't carry content
□ Section dividers or breadcrumb bar present for decks > 15 slides
□ At most two focal areas per slide (count them on the rendered image)
□ Text sizes measured on every text box: body ≥ 20 pt, drawing labels 16–18 pt, citations 12–14 pt
□ Open Sans for slide text, Solitreo inside drawings, Neo Euler for math — no other typefaces
□ Every equation typeset (Neo Euler PNG for display math, subscript runs inline) — no plain-text underscores or carets
□ Every drawing is a native shape group ("Illustration: <name>"), not a picture
□ Blue = focus, beige = context, orange = highlight — consistent on every slide
□ Nothing relies on color alone (add a mark, label or pattern too); beige fills have ink outlines
□ No broken characters (…, ·, ×, →) and no label overlapping a stroke, arrow or highlight mark
□ Drawings clear the captions and citation line
```

---

## Key Principles (Summary)

**Action titles, not topic labels.** Every slide title is a complete sentence stating the takeaway. Reading titles alone should tell the whole argument (ghost deck test).

**One argument, made well.** Don't present your whole paper. Pick the claim that can be made convincingly in the allotted time. Everything else goes in the appendix.

**One insight per slide.** One exhibit per results slide. Highlight the key finding directly on the chart — don't make the audience hunt for it.

**Slides support speech; they don't replace it.** Body text is for orientation, not information transfer. The presenter carries the argument; the slide carries the evidence.

**Cite everything borrowed.** Academic integrity applies to slides. In-text citations on the slide, full references on the References slide.

**End on conclusions.** The conclusions slide stays on screen during Q&A. Never end on "Thank You" or a blank slide.

---

## Dependencies

Same as PPTX skill:
- `pip install "markitdown[pptx]"` — text extraction
- `npm install -g pptxgenjs` — creating from scratch
- LibreOffice (`soffice`) — PDF conversion
- Poppler (`pdftoppm`, `pdftocairo`) — PDF to images

For the sketch style:
- `npm install roughjs` (work dir) and Playwright — drawings
- `lxml` (Python) — grouping drawings
- XeLaTeX with `unicode-math` — equations
- Fonts in `~/.fonts`: Solitreo, Open Sans, Neo Euler
