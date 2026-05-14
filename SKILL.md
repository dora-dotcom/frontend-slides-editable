---
name: frontend-slides-editable
description: Use when the user wants a single-file HTML presentation that stays editable in the browser after generation. Features: object drag/resize, multi-select, snap alignment, rich text toolbar, undo/redo, Pages sidebar (thumbnails, reorder, delete), image upload, background replace, Export HTML, Export PDF (fixed-px, print-quality), Ctrl+S localStorage save. Supports PPT-to-web conversion and design system auto-detection (reads design.md/brand.md/tokens.json to skip style discovery).
---

# Frontend Slides (Editable)

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser **with a built-in editor**: move objects, multi-select with **Ctrl+click**, alignment snapping, simple text formatting with **font family + size controls**, **undo/redo**, a **Pages** sidebar (slide thumbnails, drag to reorder, delete), **Ctrl+S** persistence, and **export HTML**.

This skill is a **copy of the `frontend-slides` skill** extended with the editable deck runtime. For read-only decks without editor weight, use the original **`frontend-slides`** skill instead (same skills directory layout).

## Parity with parent `frontend-slides` (style flexibility)

**Adding edit mode must not replace preset authoring.** The parent skill treats each choice in [STYLE_PRESETS.md](STYLE_PRESETS.md) as a **spec**: per preset you implement its **Layout** prose, **Signature Elements**, typography, and colors — title slides and content slides **differ across presets** (e.g. Bold Signal’s card + big numerals vs. Notebook Tabs’ paper + edge tabs vs. Swiss Modern’s grid + red bar).

**Normative behavior in Phase 3:**

1. **Read STYLE_PRESETS for the chosen preset(s)** and reflect **layout + signatures** in HTML/CSS, not only `:root` colors and fonts.
2. **The editable reference** ([examples/editable-deck-reference.html](examples/editable-deck-reference.html)) supplies **JS/CSS patterns** (chrome, sidebar, objects, history) — not a **frozen slide layout** to paste on every deck. Do **not** reuse one generic “title + subtitle + corner rounded rectangle” geometry for every style.
3. **`examples/generated/presets/*.html`** (if present) are **mechanical smoke-test builds** for the runtime; they are **not** the design target for real deliveries. Generated user decks should match **STYLE_PRESETS** expressiveness, like the parent skill.
4. **Static chrome** (decorations that should not be draggable) may live outside `.slide-edit-layer` (e.g. background pseudo-elements, fixed nav chrome) per preset; **movable** copy and blocks stay as `[data-slide-object]` inside the layer.

If runtime constraints ever conflict with a signature element, **adapt the element** (e.g. implement the same visual with CSS, or split into multiple objects) — do **not** drop preset identity for the sake of a single template.

## Context scan (run before anything else)

Before asking any questions, **scan what you already know**. The goal is to ask only for what is genuinely missing — not to run a fixed checklist regardless of context.

### Step 1 — Check for a design system

Look for any of these in the working directory (or a path the user mentioned):

```
design.md / design-system.md / brand.md / brand-guidelines.md
STYLE_GUIDE.md / style-guide.md
tokens.json / design-tokens.json / theme.json
```

**If found:** Read the file. Extract colors, fonts, spacing, and component patterns. **Skip Phase 1 Style Pref question and all of Phase 2** — the design language is already defined. Note to user: "Found `design.md` — using your design system. Skipping style selection."

**If not found:** Proceed with Phase 1–2 as normal.

### Step 2 — Score what you already know

Tally how many of the five essentials are already answered from context (conversation, attached files, CLAUDE.md, prior turns):

| Essential | Covered if… |
|---|---|
| **Purpose** | User stated audience, use case, or occasion |
| **Length** | User stated slide count, or content implies it |
| **Content** | User pasted outline, doc, or bullet points |
| **Style** | Design system found, preset named, or strong style signal given |
| **Images** | User explicitly said "no images" or provided files/links |

- **All 5 covered** → skip directly to Phase 3. Do not ask anything.
- **3–4 covered** → ask only the missing items in one short message, then proceed.
- **0–2 covered** → run the full Phase 1 grouped question, then Phase 2.

### Step 3 — Agent / programmatic invocation

If this skill is being called by an automated agent (not directly by the user typing a message), assume the invoking agent has already gathered context. Apply the same scoring above — do not re-ask questions the agent context already answers. Generate and deliver without unnecessary confirmation loops.

**The only reason to stop and ask is genuine missing information. Never ask to ask.**

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices. People discover what they want by seeing it.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides, ever. Content overflows? Split into multiple slides.

## Design Aesthetics

You tend to converge toward generic, "on distribution" outputs. In frontend design, this creates what users call the "AI slop" aesthetic. Avoid this: make creative, distinctive frontends that surprise and delight.

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use **CSS-only** animations and transitions in generated decks (this skill outputs single-file HTML, no React and no Motion library). Focus on high-impact moments: one well-orchestrated load with staggered reveals (`animation-delay`) beats scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!

## Viewport Fitting Rules

These invariants apply to EVERY slide in EVERY presentation:

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL font sizes and spacing must use `clamp(min, preferred, max)` — never fixed px/rem
- Content containers need `max-height` constraints
- Images: `max-height: min(50vh, 400px)`
- Breakpoints required for heights: 700px, 600px, 500px
- Include `prefers-reduced-motion` support
- Never negate CSS functions directly (`-clamp()`, `-min()`, `-max()` are silently ignored) — use `calc(-1 * clamp(...))` instead

**When generating, read `viewport-base.css` and include its full contents in every presentation.**

### Content Density Limits Per Slide

| Slide Type | Maximum Content |
|------------|-----------------|
| Title slide | 1 heading + 1 subtitle + optional tagline |
| Content slide | 1 heading + 4-6 bullet points OR 1 heading + 2 paragraphs |
| Feature grid | 1 heading + 6 cards maximum (2x3 or 3x2) |
| Code slide | 1 heading + 8-10 lines of code |
| Quote slide | 1 quote (max 3 lines) + attribution |
| Image slide | 1 heading + 1 image (max 60vh height) |

**Content exceeds limits? Split into multiple slides. Never cram, never scroll.**

---

## Phase 0: Detect Mode

Determine what the user wants:

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve an existing HTML presentation. Read it, understand it, enhance. **Follow Mode C modification rules below.**

### Mode C: Modification Rules

When enhancing existing presentations, viewport fitting is the biggest risk:

1. **Before adding content:** Count existing elements, check against density limits
2. **Adding images:** Must have `max-height: min(50vh, 400px)`. If slide already has max content, split into two slides
3. **Adding text:** Max 4-6 bullets per slide. Exceeds limits? Split into continuation slides
4. **After ANY modification, verify:** `.slide` has `overflow: hidden`, new elements use `clamp()`, images have viewport-relative max-height, content fits at 1280x720
5. **Proactively reorganize:** If modifications will cause overflow, automatically split content and inform the user. Don't wait to be asked

**When adding images to existing slides:** Move image to new slide or reduce other content first. Never add images without checking if existing content already fills the viewport.

---

## Phase 1: Content Discovery (New Presentations)

**Only ask for what the context scan (above) identified as missing.** If all essentials are already known, skip this phase entirely and go to Phase 2 (or Phase 3 if design system was found).

When questions are needed, send them all in one grouped message — never split across turns. Use a structured question UI when the host supports it.

**Question 1 — Purpose** *(skip if already known)*
What is this presentation for? Options: Pitch deck / Teaching-Tutorial / Conference talk / Internal presentation

**Question 2 — Length** *(skip if already known)*
Approximately how many slides? Options: Short 5-10 / Medium 10-20 / Long 20+

**Question 3 — Content** *(skip if user already provided content)*
Do you have content ready? Options: All content ready / Rough notes / Topic only
→ If they have content, ask them to paste or attach it in the same message.

**Question 4 — Style preference** *(skip if design system found or preset already named)*
What visual direction sounds closest as a starting point? Options:
- "Recommend for me" — infer from audience, topic, and content
- "Clean / Professional" — restrained, polished, trustworthy
- "Bold / Experimental" — high-contrast, energetic, surprising
- "Editorial / Warm" — human, crafted, story-forward
- "Technical / Minimal" — precise, structured, product-like
- "I already know the preset" — skip to a direct preset choice

**Question 5 — Assets / images** *(skip if user explicitly said no images or already provided them)*
Will this deck use image files you will provide? Options: **No images** (CSS/graphics only) / **Yes — I will provide images** / **Unsure — recommend**

> **Note on editing runtime:** This skill always ships the full editable runtime by default. Only ask if the user explicitly signals they want a read-only file — if so, switch to the parent `frontend-slides` skill instead.

### Step 1.2: Image Evaluation (if images provided)

If **Question 6** was **No images** or the user has not supplied any image files yet → skip to Phase 2 (you may still ask them to add images later before Phase 3 if they change their mind).

If user provides an image folder:
1. **Scan** — List all image files (.png, .jpg, .svg, .webp, etc.)
2. **Inspect each image** — Use the host's available image/file viewing capability
3. **Evaluate** — For each: what it shows, USABLE or NOT USABLE (with reason), what concept it represents, dominant colors
4. **Co-design the outline** — Curated images inform slide structure alongside text. This is NOT "plan slides then add images" — design around both from the start (e.g., 3 screenshots → 3 feature slides, 1 logo → title/closing slide)
5. **Confirm the outline in one grouped follow-up** (structured question UI when available): "Does this slide outline and image selection look right?" Options: Looks good / Adjust images / Adjust outline

**Logo in previews:** If a usable logo was identified, embed it (base64) into each style preview in Phase 2 — the user sees their brand styled three different ways.

---

## Phase 2: Style Discovery

**Skip this phase entirely if:**
- A design system file was found in the context scan → use it directly, go to Phase 3
- The user named a specific preset or provided strong visual direction → go to Phase 3
- An agent invocation already includes style context → go to Phase 3

**This is the "show, don't tell" phase** for cases where style is still open. Most people can't articulate design preferences in words.

### Step 2.0: Style Preference First

Start from the **style preference captured in Phase 1**. Before asking the user how they want to choose, give a short recommendation list of **2-4 presets** that best match their preference, audience, and content.

Use this mapping as the starting point:

| Style preference | Suggested presets |
|------|------|
| Recommend for me | Infer from purpose + audience + content, then recommend 2-4 strongest fits |
| Clean / Professional | Bold Signal, Electric Studio, Swiss Modern |
| Bold / Experimental | Creative Voltage, Neon Cyber, Split Pastel |
| Editorial / Warm | Dark Botanical, Vintage Editorial, Paper & Ink |
| Technical / Minimal | Swiss Modern, Terminal Green, Notebook Tabs |
| I already know the preset | Skip recommendation explanation and go straight to preset picking |

Explain the recommendation briefly in concrete terms, for example: audience fit, energy level, brand tone, or content density.

If the user already chose **"I already know the preset"** in Phase 1, skip Step 2.1 and go straight to the preset picker.

### Step 2.1: Style Path

Ask how they want to choose (header: "Style"):
- "Pick from recommendations" (recommended) — Choose directly from the suggested presets
- "Show me options" — Generate 3 previews based on the recommended direction
- "I know what I want" — Pick from the full preset list directly

**If direct selection:** Show preset picker and skip to Phase 3. Available presets are defined in [STYLE_PRESETS.md](STYLE_PRESETS.md).

### Step 2.2: Mood Selection (Guided Discovery)

Ask (header: "Vibe", multiSelect: true, max 2):
What feeling should the audience have? Options:
- Impressed/Confident — Professional, trustworthy
- Excited/Energized — Innovative, bold
- Calm/Focused — Clear, thoughtful
- Inspired/Moved — Emotional, memorable

Use the user's style preference and recommended preset cluster to steer this question. If the preference already strongly determines the direction, keep the previews within that neighborhood instead of scattering across unrelated aesthetics.

### Step 2.3: Generate 3 Style Previews

Based on mood **and the earlier style preference**, generate 3 distinct single-slide HTML previews showing typography, colors, animation, and overall aesthetic. Read [STYLE_PRESETS.md](STYLE_PRESETS.md) for available presets and their specifications.

| Mood | Suggested Presets |
|------|-------------------|
| Impressed/Confident | Bold Signal, Electric Studio, Dark Botanical |
| Excited/Energized | Creative Voltage, Neon Cyber, Split Pastel |
| Calm/Focused | Notebook Tabs, Paper & Ink, Swiss Modern |
| Inspired/Moved | Dark Botanical, Vintage Editorial, Pastel Geometry |

Save previews under a **project-local** scratch folder (e.g. `.claude-design-slide-previews/` or `.design/slide-previews/`) as `style-a.html`, `style-b.html`, `style-c.html`. Each should be self-contained, ~50-100 lines, showing one animated title slide.

Open each preview in the default browser when possible: **macOS** `open path/to/file.html`; **Linux** `xdg-open path/to/file.html`; **Windows** `start path\to\file.html`.

When possible, keep at least **2 of the 3 previews** within the recommended preset family so the user sees relevant variations before they see outliers.

### Step 2.4: User Picks

Ask (header: "Style"):
Which style preview do you prefer? Options: Style A: [Name] / Style B: [Name] / Style C: [Name] / Mix elements

If "Mix elements", ask for specifics.

---

## Phase 3: Generate Presentation

Generate the full presentation using content from Phase 1 (text, or text + curated images) and style from Phase 2.

If images were provided, the slide outline already incorporates them from Step 1.2. If not, CSS-generated visuals (gradients, shapes, patterns) provide visual interest — this is a fully supported first-class path.

**Before generating, read these supporting files:**
- [STYLE_PRESETS.md](STYLE_PRESETS.md) — **Authoritative visual spec** for the chosen preset (layout, signature, fonts, colors) — same role as in parent `frontend-slides`
- [editor-runtime.md](editor-runtime.md) — **DOM contract** (`data-slide-object`, `data-oid`, edit layer), history types, snap rules, generator checklist
- [examples/editable-deck-reference.html](examples/editable-deck-reference.html) — **Copy the deck runtime** (editor + sidebar + history + persistence patterns); **do not** treat its slide markup as the only allowed layout
- [html-template.md](html-template.md) — HTML architecture and integration notes
- [viewport-base.css](viewport-base.css) — Mandatory CSS (include in full)
- [animation-patterns.md](animation-patterns.md) — Animation reference for the chosen feeling

**Key requirements:**
- Single self-contained HTML file, all CSS/JS inline
- Include the FULL contents of viewport-base.css in the `<style>` block
- **Preset fidelity:** Implement **Layout** and **Signature Elements** from [STYLE_PRESETS.md](STYLE_PRESETS.md) for the selected style. Vary structure slide-to-slide and preset-to-preset; avoid a **single repeated title-slide prototype** across all aesthetics (parent skill does not do that).
- **Every slide** `section.slide` must have a stable `id`; movable content lives in `.slide-edit-layer` as `[data-slide-object][data-oid]` per [editor-runtime.md](editor-runtime.md)
- **Deck slide list:** Never use a global `querySelectorAll('section.slide')` when a filmstrip clones slides — use only slides under the deck wrapper (e.g. `.slides-offset` + `:scope > section.slide`). See [html-template.md](html-template.md) §Regression guard.
- Embed the **editable deck runtime** (from the reference example): `SlideDeck`, object editor (select / drag / snap / RTE toolbar), `SlideSidebar`, `HistoryStack`, save/export. The sidebar **must** include both `#btnExport` (HTML) and `#btnExportPdf` (PDF), wired to the `exportHtml()` and `exportPdf()` functions copied verbatim from the reference. Do not invent a custom PDF implementation — copy it directly.
- Use fonts from Fontshare or Google Fonts — never system fonts
- Add detailed comments explaining each section
- Every section needs a clear `/* === SECTION NAME === */` comment block

---

## Phase 4: PPT Conversion

When converting PowerPoint files:

1. **Extract content** — Run `python3 scripts/extract-pptx.py <input.pptx> <output_dir>` (install python-pptx if needed: `pip install python-pptx`)
2. **Confirm with user** — Present extracted slide titles, content summaries, and image counts
3. **Style selection** — Proceed to Phase 2 for style discovery
4. **Generate HTML** — Convert to chosen style, preserving all text, images (from assets/), slide order, and speaker notes (as HTML comments)

---

## Phase 5: Delivery

1. **Clean up** — Delete the temporary slide-previews folder (see Phase 2) if it exists
2. **Smoke check (quick)** — Before handing off: open the file once; confirm **no in-slide scrolling** at ~1280×720; in edit mode, open **Pages**, reorder one slide and refresh — **no duplicate slides** (regression guard); **Export HTML** opens and runs standalone; **Export PDF** opens a new tab and auto-prints. If PDF is missing or broken, check the browser console — the startup self-check will log `[deck-runtime] Missing required element: #btnExportPdf` (or similar) to identify the gap; fix before delivering.
3. **Open** — Launch in default browser: **macOS** `open [filename].html`; **Linux** `xdg-open [filename].html`; **Windows** `start [filename].html`
4. **Summarize** — Tell the user:
   - File location, style name, slide count
   - Navigation: Arrow keys, Space, scroll/wheel (wheel disabled while edit mode on), click nav dots
   - **Edit mode:** `E` enters edit mode. **Hover the top-left** to reveal **Edit**, **Pages**, and (while editing) **Undo** / **Redo** / **Done**; controls hide after the pointer leaves (~400ms). **Done** (same cluster) exits edit mode — the **Edit** button label stays **Edit**. **Esc** blurs text first, then exits edit mode when not typing in a text box
   - **Pages** sidebar for thumbnails, reorder (drag rows), delete slides
   - **Objects:** drag **⠿** to move; drag **corner resize** on selected objects to change width/height (text reflows); **Ctrl+click** multi-select (macOS: **Control** key); **Delete/Backspace** removes selection (confirm if 2+)
   - **Snap:** aligns to **slide center** and **other objects** — not to the outer slide edges
   - **Text:** click text to type; floating toolbar for bold/italic/**font**/**size** (visible with caret, no need to select a range); **Ctrl+Z** / **Ctrl+Y** or **Ctrl+Shift+Z**; **Cmd+Z** / **Cmd+Y** / **Cmd+Shift+Z** on macOS when not typing in `contenteditable`
   - **Save** (`#btnSave`, top-left next to **Edit** / **Pages** when editing — same hover reveal) or **Ctrl+S** / **Cmd+S** saves the full deck structure to localStorage
   - **Pages sidebar** (in edit mode) contains: **＋ Add Image** (uploads an image as a new object on the current slide), **Export PDF** (choose 16:9 or 4:3 → opens a fixed-px print page in a new tab → auto-prints), **Export HTML** (clean standalone file, strips edit state)
   - **Images:** double-click any graphic object to replace its image; slides with a replaceable background show a **📷 Replace background** button when edit mode is on (hover the left panel)
   - How to customize: slide theme `:root` variables, **`--deck-chrome-*`** for edit UI (see [STYLE_PRESETS.md](STYLE_PRESETS.md) §Deck chrome tokens), font link, `.reveal` animations; keep `data-oid` unique when adding objects

---

## Supporting Files

| File | Purpose | When to Read |
|------|---------|-------------|
| [editor-runtime.md](editor-runtime.md) | DOM contract, undo types, snap rules, generator checklist | Phase 3 (before codegen) |
| [examples/editable-deck-reference.html](examples/editable-deck-reference.html) | Working reference: full runtime in one file | Phase 3 (copy/adapt JS/CSS) |
| [STYLE_PRESETS.md](STYLE_PRESETS.md) | 12 curated visual presets with colors, fonts, and signature elements | Phase 2 (style selection) |
| [viewport-base.css](viewport-base.css) | Mandatory responsive CSS — copy into every presentation | Phase 3 (generation) |
| [html-template.md](html-template.md) | HTML structure, integration with editable runtime | Phase 3 (generation) |
| [animation-patterns.md](animation-patterns.md) | CSS/JS animation snippets and effect-to-feeling guide | Phase 3 (generation) |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | Python script for PPT content extraction | Phase 4 (conversion) |
| [README.md](README.md) | Bilingual extended overview, comparison table, troubleshooting | Optional (users / maintainers) |
