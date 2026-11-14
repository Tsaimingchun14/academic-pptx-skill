# Slide Patterns for Academic Presentations

Implementation patterns for each required slide type. Use with `pptxgenjs.md` for the technical API.

All coordinates assume `LAYOUT_16x9` (10" × 5.625"). Adjust proportionally for other layouts.

---

## Global Defaults

Apply these to every slide in an academic deck:

```javascript
const COLORS = {
  bg:       "FAF9F6",   // Paper (off-white) — every slide, no dark slides
  primary:  "1E1E1E",   // Ink — titles, outlines
  accent:   "2F6FD8",   // Blue — the focus of the slide, section headers
  body:     "2B2B2B",   // Body text
  muted:    "737373",   // Citations, captions (4.5:1 on paper)
  fill:     "E9D8C0",   // Beige — context objects, comparison bars (always ink-outlined)
  lightFill:"F3EADD",   // Light beige — panels, callout boxes
  highlight:"D9731A",   // Orange — hand-drawn "look here" marks
};

const FONTS = {
  face: "Open Sans",     // All slide text outside drawings (set as theme font too)
  draw: "Solitreo",      // Labels inside drawings
  title: 26,             // Action title: 24–28 pt
  sectionHeader: 22,     // Within-slide section headers
  body: 20,              // Body bullets: 20 pt minimum
  label: 16,             // Chart annotations, inline labels
  cite: 13,              // In-slide citations, footnotes
};
// Math: Neo Euler PNGs from scripts/render_equation.py (see SKILL.md)
// Drawings and charts: rough.js → editable shape groups via scripts/ (see SKILL.md)

pres.theme = { headFontFace: FONTS.face, bodyFontFace: FONTS.face };
const MARGIN = 0.5;      // Minimum margin from slide edge (inches)
// Every slide
slide.background = { color: COLORS.bg };
```

---

## 1. Title Slide

**Purpose:** Establish the presentation; give the audience complete attribution.

```javascript
// Same paper background as every other slide (no dark slides)
slide.background = { color: COLORS.bg };

// Main title — framed as a statement or question
slide.addText("Treatment effect of early childhood interventions\npersists into adulthood across all income quartiles", {
  x: 0.7, y: 1.4, w: 8.6, h: 1.8,
  fontSize: 32, fontFace: FONTS.face, color: COLORS.primary,
  bold: true, align: "left", valign: "top"
});

// Subtitle / conference context
slide.addText("Annual Conference of the Society for Labor Economics  ·  May 2025", {
  x: 0.7, y: 3.2, w: 8.6, h: 0.4,
  fontSize: 16, fontFace: FONTS.face, color: COLORS.accent,
  align: "left"
});

// Author and affiliation
slide.addText("Jane Smith¹  ·  John Doe²\n¹ University of X   ²aboratory for Y", {
  x: 0.7, y: 3.7, w: 8.6, h: 0.6,
  fontSize: 15, fontFace: FONTS.face, color: COLORS.body,
  align: "left"
});

// Optional: a small hand-drawn sketch of the topic on the right (scripts/vec.js)
// addIllustration(pres, slide, "out/hero.json", 6.2, 1.2, 1, "<what it shows>");
```

**Do not include:** Decorative images, animated logos, institution crests (unless explicitly requested), clip art.

---

## 2. Motivation / Context Slide

**Purpose:** Establish the situation and complication — why this question matters and what's missing.

Layout: Two-column (context left, gap/problem right) or single-column narrative. Use single-column for most conference talks.

```javascript
// Action title
slide.addText("Existing interventions show strong short-run effects but evidence on persistence is sparse", {
  x: MARGIN, y: 0.2, w: 9.0, h: 0.8,
  fontSize: FONTS.title, fontFace: FONTS.face, color: COLORS.primary, bold: true, valign: "top"
});

// Body bullets
slide.addText([
  { text: "Short-run gains well established: ", options: { bold: true, breakLine: false } },
  { text: "meta-analyses confirm positive effects at ages 5–8 (Heckman et al. 2013).", options: { breakLine: true } },
  { text: "Long-run evidence is scarce: ", options: { bold: true, breakLine: false } },
  { text: "only 3 RCTs track outcomes past age 25; none cover lower-income countries.", options: { breakLine: true } },
  { text: "Mechanism is unresolved: ", options: { bold: true, breakLine: false } },
  { text: "cognitive vs. non-cognitive channels remain debated (see Appendix A).", options: { breakLine: true } },
], {
  x: MARGIN, y: 1.1, w: 9.0, h: 3.2,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  bullet: true, paraSpaceAfter: 12
});

// In-slide citation
slide.addText("Heckman et al. (2013), Science; Cunha & Heckman (2007), AER", {
  x: MARGIN, y: 5.1, w: 9.0, h: 0.35,
  fontSize: FONTS.cite, fontFace: FONTS.face, color: COLORS.muted, align: "left"
});
```

---

## 3. Research Question Slide

**Purpose:** Give the audience the anchor they need to evaluate everything that follows. This slide must exist on its own.

```javascript
// Action title
slide.addText("This paper asks: do early childhood effects persist to age 35,\nand through which channels?", {
  x: MARGIN, y: 0.2, w: 9.0, h: 0.9,
  fontSize: FONTS.title, fontFace: FONTS.face, color: COLORS.primary, bold: true
});


// Research question in a prominent callout box
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 1.5, y: 1.4, w: 7.0, h: 1.6,
  fill: { color: COLORS.lightFill }, line: { color: COLORS.primary, pt: 1.5 }, rectRadius: 0.1
});

slide.addText("Do effects of the X program on cognitive and socio-emotional skills\nat age 8 persist to age 35 outcomes (earnings, health, crime),\nand does the pathway run through skills or through schooling attainment?", {
  x: 1.7, y: 1.55, w: 6.6, h: 1.3,
  fontSize: 19, fontFace: FONTS.face, color: COLORS.primary,
  bold: false, align: "center", valign: "middle"
});

// Optional: brief note on what makes this paper's approach novel
slide.addText([
  { text: "Contribution: ", options: { bold: true, breakLine: false } },
  { text: "First study to follow a randomized cohort from ages 3–5 to 35; administrative earnings and health records linked to original experimental data.", options: {} }
], {
  x: MARGIN, y: 3.2, w: 9.0, h: 1.0,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body
});
```

---

## 4. Methods Slide

**Purpose:** Give the audience what they need to evaluate the findings — not procedural completeness.

Target: 1–2 slides. Move all detail the audience doesn't need to Appendix.

```javascript
// Action title
slide.addText("Regression discontinuity exploits a sharp household income threshold\nfor program eligibility — treatment is as-good-as-random near the cutoff", {
  x: MARGIN, y: 0.2, w: 9.0, h: 0.9,
  fontSize: FONTS.title, fontFace: FONTS.face, color: COLORS.primary, bold: true
});


// Two-column: design on left, key variables on right
// Left column header
slide.addText("Design", {
  x: MARGIN, y: 1.25, w: 4.2, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

slide.addText([
  { text: "Cohort: ", options: { bold: true, breakLine: false } },
  { text: "2,400 children born 1985–90 in three counties", options: { breakLine: true } },
  { text: "Assignment: ", options: { bold: true, breakLine: false } },
  { text: "income < 185% FPL at age 3 → eligible (N = 1,150)", options: { breakLine: true } },
  { text: "Follow-up: ", options: { bold: true, breakLine: false } },
  { text: "ages 5, 8, 18, 25, 35 — admin records linked", options: { breakLine: true } },
], {
  x: MARGIN, y: 1.65, w: 4.2, h: 2.4,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  bullet: true, paraSpaceAfter: 10
});

// Right column header
slide.addText("Key outcomes", {
  x: 5.3, y: 1.25, w: 4.2, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

slide.addText([
  { text: "Primary: ", options: { bold: true, breakLine: false } },
  { text: "age-35 earnings (log), employment", options: { breakLine: true } },
  { text: "Secondary: ", options: { bold: true, breakLine: false } },
  { text: "health index, criminal record indicator", options: { breakLine: true } },
  { text: "Mechanism: ", options: { bold: true, breakLine: false } },
  { text: "cognitive score age 8, years of schooling", options: { breakLine: true } },
], {
  x: 5.3, y: 1.65, w: 4.2, h: 2.4,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  bullet: true, paraSpaceAfter: 10
});

// Appendix pointer
slide.addText("Full identification assumptions and robustness checks → Appendix B", {
  x: MARGIN, y: 5.1, w: 9.0, h: 0.35,
  fontSize: FONTS.cite, fontFace: FONTS.face, color: COLORS.muted, align: "left"
});
```

---

## 5. Results Slide

**Purpose:** Present one finding, make it impossible to miss.

Layout: Figure left (~5.5"), interpretive text right (~3.5"). Action title states the result.

```javascript
// Action title — MUST state the finding, not just the topic
slide.addText("Treated children earn 18% more at age 35 — effect is largest in the bottom income quartile", {
  x: MARGIN, y: 0.2, w: 9.0, h: 0.85,
  fontSize: FONTS.title, fontFace: FONTS.face, color: COLORS.primary, bold: true
});


// FIGURE (left side) — a hand-drawn rough.js chart rebuilt as editable shapes.
// Define it in illus.js (bars in beige, the focal bar in blue, values written on the bars,
// Solitreo labels) and mark the key finding with an orange highlight, e.g.:
//   effect: { w: 540, h: 380, draw() {
//     [["Q1", 28], ["Q2", 22], ["Q3", 15], ["Q4", 8]].forEach(([q, v], i) => {
//       const x = 50 + i * 120, top = 330 - v * 10;
//       rect(x, top, 80, v * 10, { fill: i === 0 ? BLUE : BEIGE });
//       text(x + 40, top - 10, v + "%", { anchor: "middle", color: i === 0 ? BLUE : INK });
//       text(x + 40, 362, q, { anchor: "middle" });
//     });
//     line(30, 330, 520, 330);
//     hlLoop(90, 32, 90, 50);                       // KEY FINDING — tell the audience what to see
//   } }
// Render with scripts/render_illustrations.py, then place it:
addIllustration(pres, slide, "out/effect.json", MARGIN, 1.15, 1,
  "Bar chart of earnings effect by income quartile: Q1 28%, Q2 22%, Q3 15%, Q4 8%; Q1 highlighted");
// If the user supplied a finished plot instead, insert it as given (cropped, readable, cited):
// slide.addImage({ path: "user_plot.png", x: MARGIN, y: 1.15, w: 5.4, h: 3.8, altText: "..." });

// INTERPRETIVE TEXT (right side)
slide.addText("What to take away", {
  x: 6.2, y: 1.15, w: 3.3, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

slide.addText([
  { text: "Average effect: 18% earnings gain (p < 0.001)", options: { breakLine: true } },
  { text: "Heterogeneity: effects are 3.5× larger for Q1 vs Q4", options: { breakLine: true } },
  { text: "Precision: 95% CI = [14%, 22%] for pooled estimate", options: { breakLine: true } },
], {
  x: 6.2, y: 1.55, w: 3.3, h: 2.5,
  fontSize: FONTS.body - 1, fontFace: FONTS.face, color: COLORS.body,
  bullet: true, paraSpaceAfter: 12
});

// In-slide citation
slide.addText("Administrative earnings records, Social Security Administration (accessed 2024)", {
  x: MARGIN, y: 5.15, w: 9.0, h: 0.3,
  fontSize: FONTS.cite, fontFace: FONTS.face, color: COLORS.muted
});
```

**Critical checks for results slides:**
- Action title states the finding, not the topic
- Key result is marked directly on the chart with an orange hand-drawn highlight (loop, underline, arrow or box)
- Source cited at the bottom
- No second chart or second finding on the same slide

---

## 6. Discussion / Implications Slide

**Purpose:** Interpret the findings; connect back to the opening question; address the main limitation.

```javascript
// Action title
slide.addText("Results support a skill-formation pathway: the earnings effect is fully mediated\nby cognitive scores at age 8, not by schooling attainment", {
  x: MARGIN, y: 0.2, w: 9.0, h: 0.9,
  fontSize: FONTS.title, fontFace: FONTS.face, color: COLORS.primary, bold: true
});


// Interpretation
slide.addText("Interpretation", {
  x: MARGIN, y: 1.2, w: 9.0, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

slide.addText([
  { text: "Consistent with Cunha-Heckman (2007) skill complementarity: early investment compounds through the schooling years.", options: { breakLine: true } },
  { text: "Schooling channel: coefficient falls to zero when conditioning on age-8 cognitive score (mediation analysis, Appendix C).", options: { breakLine: true } },
], {
  x: MARGIN, y: 1.6, w: 9.0, h: 1.3,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  bullet: true, paraSpaceAfter: 10
});

// Main limitation — address it directly
slide.addText("Main limitation", {
  x: MARGIN, y: 3.0, w: 9.0, h: 0.35,
  fontSize: FONTS.sectionHeader, fontFace: FONTS.face, color: COLORS.accent, bold: true
});

slide.addText([
  { text: "External validity: ", options: { bold: true, breakLine: false } },
  { text: "program was implemented in three U.S. counties; generalizability to other settings requires caution.", options: { breakLine: true } },
  { text: "Partial identification: ", options: { bold: true, breakLine: false } },
  { text: "earnings records unavailable for 11% of cohort (attrition analysis → Appendix D).", options: { breakLine: true } },
], {
  x: MARGIN, y: 3.4, w: 9.0, h: 1.3,
  fontSize: FONTS.body, fontFace: FONTS.face, color: COLORS.body,
  bullet: true, paraSpaceAfter: 10
});
```

---

## 7. Conclusions Slide

**Purpose:** Restate the 2–4 key takeaways. **This slide stays on screen for the entire Q&A.**

Do not follow it with "Thank You," a blank slide, or a transition to appendix slides during Q&A.

```javascript
// Same paper background as every slide (no dark slides)
slide.background = { color: COLORS.bg };

// "Conclusions" label
slide.addText("Conclusions", {
  x: MARGIN, y: 0.25, w: 9.0, h: 0.45,
  fontSize: 20, fontFace: FONTS.face, color: COLORS.accent, bold: true, align: "left"
});

// Optional: a small hand-drawn icon beside each takeaway (scripts/vec.js), e.g.
// addIllustration(pres, slide, "out/takeaway1.json", MARGIN, 0.95, 1, "<what it shows>");

// Key takeaways — numbered for easy reference during Q&A
slide.addText([
  { text: "1. Early childhood effects are persistent: ", options: { bold: true, breakLine: false } },
  { text: "a significant earnings premium is detectable at age 35, 30 years after treatment.", options: { breakLine: true, breakLine: true } },
  { text: "2. Effects are largest for the most disadvantaged: ", options: { bold: true, breakLine: false } },
  { text: "the Q1 earnings premium (28%) is 3.5× the Q4 effect (8%).", options: { breakLine: true, breakLine: true } },
  { text: "3. The pathway is cognitive, not schooling-mediated: ", options: { bold: true, breakLine: false } },
  { text: "consistent with skill complementarity models.", options: { breakLine: true } },
], {
  x: MARGIN, y: 0.85, w: 9.0, h: 3.5,
  fontSize: FONTS.body + 1, fontFace: FONTS.face, color: COLORS.body,
  paraSpaceAfter: 20
});

// Contact + link
slide.addText("jane.smith@university.edu  |  Working paper: bit.ly/smith2025", {
  x: MARGIN, y: 4.8, w: 7.0, h: 0.4,
  fontSize: 14, fontFace: FONTS.face, color: COLORS.muted, align: "left"
});

// Optional QR code (add as image)
// slide.addImage({ path: "qr_preprint.png", x: 8.5, y: 4.5, w: 0.9, h: 0.9 });
```

---

## 8. Section Divider (for decks > 15 slides)

**Purpose:** Orient the audience at the start of each major section.

```javascript
// Same paper background as every slide (no dark slides)
slide.background = { color: COLORS.bg };

// Section number / label
slide.addText("Part 2", {
  x: MARGIN, y: 1.8, w: 9.0, h: 0.4,
  fontSize: 16, fontFace: FONTS.face, color: COLORS.accent, bold: false, align: "left"
});

// Section title
slide.addText("Empirical Strategy", {
  x: MARGIN, y: 2.2, w: 9.0, h: 1.0,
  fontSize: 36, fontFace: FONTS.face, color: COLORS.primary, bold: true, align: "left"
});

// Optional: a hand-drawn underline in the highlight color instead of a ruled line
// (draw it as part of a small illustration with hlUnderline from scripts/draw_helpers.js)
```

---

## 9. Breadcrumb Bar (optional, for long talks)

A persistent header strip showing the current section. Add to every content slide for talks > 15 minutes.

```javascript
// Add to each slide after the title/divider set
const sections = ["Motivation", "Data", "Strategy", "Results", "Discussion"];
const currentSection = "Results";  // Changes per slide

const barY = 0.0;
const barH = 0.28;

// Background bar
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: barY, w: 10, h: barH,
  fill: { color: COLORS.lightFill }, line: { color: COLORS.lightFill }
});

// Section labels
const sectionW = 10 / sections.length;
sections.forEach((section, i) => {
  const isActive = section === currentSection;
  slide.addText(section, {
    x: i * sectionW, y: barY, w: sectionW, h: barH,
    fontSize: 10, fontFace: FONTS.face,
    color: isActive ? COLORS.accent : COLORS.muted,
    bold: isActive,
    align: "center", valign: "middle"
  });
  // Active section underline
  if (isActive) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: i * sectionW + sectionW * 0.1, y: barY + barH - 0.04, w: sectionW * 0.8, h: 0.04,
      fill: { color: COLORS.accent }
    });
  }
});

// Shift all other content down by barH to avoid collision
// (adjust y coordinates in the rest of the slide by +barH)
```

---

## 10. References Slide

**Purpose:** Complete citations for all sources cited in the deck. Required.

```javascript
slide.background = { color: COLORS.bg };

slide.addText("References", {
  x: MARGIN, y: 0.2, w: 9.0, h: 0.5,
  fontSize: 24, fontFace: FONTS.face, color: COLORS.primary, bold: true
});


const refs = [
  "Cunha, F. & Heckman, J.J. (2007). The Technology of Skill Formation. American Economic Review, 97(2), 31–47.",
  "Heckman, J.J., Moon, S.H., Pinto, R., Savelyev, P.A., & Yavitz, A. (2013). The Rate of Return to the HighScope Perry Preschool Program. Journal of Public Economics, 94(1), 114–128.",
  "Smith, J. & Doe, J. (2025). Long-Run Returns to Early Childhood Intervention: Evidence from a Randomized Trial. Working paper.",
];

const refItems = refs.flatMap((r, i) => [
  { text: r, options: { breakLine: true } },
  ...(i < refs.length - 1 ? [{ text: "", options: { breakLine: true } }] : [])
]);

slide.addText(refItems, {
  x: MARGIN, y: 0.85, w: 9.0, h: 4.5,
  fontSize: 13, fontFace: FONTS.face, color: COLORS.body,
  paraSpaceAfter: 8
});
```

---

## 11. Appendix Slide

**Purpose:** Pre-built answer slides. Label clearly so they can be navigated to quickly during Q&A.

```javascript
// Appendix label — muted to distinguish from main deck
slide.addText("Appendix B — Robustness Checks", {
  x: MARGIN, y: 0.15, w: 9.0, h: 0.4,
  fontSize: 14, fontFace: FONTS.face, color: COLORS.muted, bold: false, italics: true
});

// Action title (still required — appendix slides also use action titles)
slide.addText("Earnings effect is stable across bandwidth choices and polynomial specifications", {
  x: MARGIN, y: 0.6, w: 9.0, h: 0.75,
  fontSize: FONTS.title - 2, fontFace: FONTS.face, color: COLORS.primary, bold: true
});

// Content follows normal slide patterns
```

---

## Quick Checks Before Delivery

```
□ Title slide: full title as statement/question, author, affiliation, venue, date
□ Every content slide: action title (complete sentence, states takeaway)
□ Ghost deck test: titles alone tell the complete argument
□ Results slides: one exhibit each, key finding annotated on the chart
□ Every borrowed figure/data point: in-slide citation
□ References slide: complete, consistently formatted
□ Conclusions slide: last main slide, stays on screen during Q&A
□ Contact info / QR code on conclusions or final slide
□ Body text ≥ 20 pt throughout
□ No slide has > ~40 words of body text
□ Appendix slides labeled, with pre-built Q&A answers
□ Deck runs 1–2 minutes under the time limit when practiced aloud
```
