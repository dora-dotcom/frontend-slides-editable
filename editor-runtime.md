# Editable deck runtime — DOM contract & integration

Use this document when generating HTML with **frontend-slides-editable**. The canonical copy-paste implementation lives in [examples/editable-deck-reference.html](examples/editable-deck-reference.html).

**Style vs. runtime:** This file defines **how** objects and chrome behave, not **what** each preset looks like. Generators must still follow [STYLE_PRESETS.md](STYLE_PRESETS.md) **Layout** and **Signature Elements** per preset (same expectation as parent `frontend-slides`). Copy **runtime** from the reference; do **not** clone its sample slide geometry for every aesthetic.

## When to include the runtime

This skill **always** ships presentations with the editable deck (edit mode, sidebar, undo, export). Omit only if the user explicitly asks for a read-only deck (rare); then follow the parent `frontend-slides` skill instead.

## Deck chrome tokens (`--deck-chrome-*`)

Fixed UI (progress bar, nav dots, **edit top bar**, sidebar, RTE, object handles, export bar) must **not** hardcode colors that only match one slide theme. Use CSS variables on `:root`:

| Variable | Typical use |
|----------|-------------|
| `--deck-chrome-bg` | Panels, semi-opaque bars |
| `--deck-chrome-border` | Borders on chrome controls |
| `--deck-chrome-text` | Labels, icon color (`currentColor` in SVG) |
| `--deck-chrome-muted` | Secondary labels |
| `--deck-chrome-accent` | Primary action, selection outline, resize handle |
| `--deck-chrome-shadow` | Drop shadow on floating chrome |
| `--deck-chrome-surface` | Button / input surfaces |

Slide **content** theme uses separate tokens (e.g. `--slide-bg-deep`, `--slide-bg-gradient`, `--text-primary` in the reference). **Phase 3 merge order:** `viewport-base.css` → preset `:root` (slide theme) → map or define `--deck-chrome-*` → runtime chrome CSS (using `var(--deck-chrome-*)` only).

**Surfaces that must not steal object clicks:** Mark chrome containers with `data-deck-chrome-surface` where focus/click routing matters; the reference uses it on `#rteToolbar` and `#deckEditChrome` for documentation and optional scripting.

## DOM contract

### Slide root

- Each slide is a `<section class="slide" id="slide-N">` (stable `id` required for persistence).
- `position: relative` is already set by `viewport-base.css` on `.slide`.
- **Deck queries:** Runtime code must list slides only under the deck root (e.g. `.slides-offset` with `:scope > section.slide`). Thumbnail previews clone `<section class="slide">` into the sidebar; a global `querySelectorAll('section.slide')` will include those clones and break navigation, reorder, and refresh (duplicate slides).

### Edit layer

- Direct child of each slide (or after background layers):

```html
<div class="slide-edit-layer" aria-hidden="true"></div>
```

- CSS: `position: absolute; inset: 0; z-index: 5; pointer-events: none;`
- In **edit mode**, children with `pointer-events: auto` receive clicks; the layer itself stays `pointer-events: none` so clicks pass through empty areas to a **slide hit target** (optional full-size transparent child) only if you need “click empty to deselect” — the reference uses the layer with `pointer-events: none` and listens on `section.slide` for background hits.

### Slide objects (`data-slide-object`)

Every independently movable / selectable block **must** include a move handle and a resize handle (reference injects resize if missing via `ensureResizeHandles` on load / edit-on).

```html
<div
  class="slide-object"
  data-slide-object
  data-oid="s0-o0"
  data-object-type="text"
  style="position:absolute;left:8%;top:15%;width:80%;min-height:1em;"
>
  <button type="button" class="slide-object-move" aria-label="Move object" title="Drag to move">⠿</button>
  <button type="button" class="slide-object-resize" aria-label="Resize"></button>
  <div class="slide-object-text" contenteditable="false">Editable text</div>
</div>
```

| Attribute | Required | Meaning |
|-----------|----------|---------|
| `data-slide-object` | yes | Marker for editor |
| `data-oid` | yes | Unique string in the **whole document** (e.g. `s2-o1`) |
| `data-object-type` | recommended | `text` (inner `.slide-object-text`) or `graphic` (no rich text; whole box draggable) |

**Text reflow:** `.slide-object-text` should use `width: 100%`, `box-sizing: border-box`, `overflow-wrap: anywhere` (and/or `word-break`) so changing the object’s width via resize updates line breaks without inner scroll.

**Graphics / images:**

```html
<div class="slide-object" data-slide-object data-oid="s0-o2" data-object-type="graphic"
     style="position:absolute;left:50%;top:40%;width:200px;height:120px;">
  <button type="button" class="slide-object-move" aria-label="Move object">⠿</button>
  <button type="button" class="slide-object-resize" aria-label="Resize"></button>
  <div class="slide-object-graphic">
    <img src="assets/x.png" alt="" style="max-height:min(40vh,300px);width:100%;object-fit:contain;pointer-events:none;">
  </div>
</div>
```

The snippet uses fixed `px` for brevity; when **generating** new decks, prefer **`%` or `clamp(...)`** on the outer `.slide-object` box where practical so layout stays consistent with viewport rules in `SKILL.md`.

- Position with `left` / `top` as **`%` of slide** (reference normalizes on drag end). `width` / `height` may be `%` or `px`; resize writes **`%` of slide** for consistency.

### Top-left control cluster (`#deckLeftHover`)

Controls are grouped in a **fixed top-left** container. **Opacity / pointer-events:** **Edit**, **Pages**, and (in edit mode) **#deckEditChrome** (Undo / Redo / Done) use the same **hover-reveal** pattern: moving the pointer into `#deckLeftHover` adds a `.show` class; `mouseleave` + ~400ms delay removes it (including while edit mode is on), matching the original “corner to reveal” behavior.

- **Edit** — enters edit mode only (label stays **Edit**; do not duplicate **Done** on this button).
- **Done** — only on `#deckEditChrome`; exits edit mode.
- **Undo** / **Redo** — icon buttons, `disabled` when stack empty; `HistoryStack` notifies via `onChange` callback.

`z-index` should stay **above** slide decorations so presets with corner marks remain readable.

### Object position for drag / undo (`left` / `top`)

`getComputedStyle(el).left` is usually **px**, not `%`, even when the author set `%` in the `style` attribute. The reference uses **`_positionPct(el, slide, 'left'|'top')`**: read `%` from **inline** `el.style` when present; otherwise derive from `getBoundingClientRect()` vs the slide rect. Using `?? 0` on failed parse causes a jump to the slide’s top-left on drag start.

### Edit mode CSS hooks

- `body.deck-edit-mode` — editor active; reference shows handles, sidebar, disables wheel navigation.
- `.slide-object.is-selected` — selected object (multi-select: multiple elements have this class). **Resize handle** is visible only when selected (`body.deck-edit-mode .slide-object.is-selected .slide-object-resize`).
- `body.deck-sidebar-open` — reserve `padding-right` on slides container for the filmstrip.

## History command types (undo / redo)

| `type` | Payload (conceptually) | Undo behavior |
|--------|------------------------|---------------|
| `moveGroup` | `{ entries: [{ oid, left, top }] }` before or after snapshot | Restore previous `left`/`top` |
| `patchObject` | `{ oid, html }` or `{ oid, style: { left, top, width, height } }` | Restore prior fragment / dimensions |
| `deleteGroup` | `{ snapshots: [{ parentSelector, index, outerHTML }] }` | Re-insert nodes |
| `reorderSlides` | `{ fromIndex, toIndex }` | Move slide section back |
| `deleteSlide` | `{ index, outerHTML, nextSiblingId }` | Re-insert section |

The reference implementation uses a **command stack** with `undo()` / `redo()` applying inverse operations. **`push()` clears the redo stack** and invokes an `onChange` callback (use it to sync undo/redo button `disabled` state).

## Snap alignment (reference behavior)

- **Snap threshold:** 8px (`SNAP_PX`), skipped when `prefers-reduced-motion: reduce`.
- **Slide guides:** Only **horizontal and vertical center** of the slide (`width/2`, `height/2`). **Slide outer edges are not snap targets** — avoids objects snapping to the viewport boundary when near the edge.
- **Object guides:** Edges and centers of **other** `data-slide-object` on the same slide (excluding the moving selection).
- Snapping adjusts the **drag delta** for the whole group so the **primary dragged element** aligns; siblings get the same delta.

## RTE (rich text toolbar)

- Toolbar `#rteToolbar` is shown when a `.slide-object-text[contenteditable="true"]` is **focused** or when the selection/caret is inside such an element (including **collapsed** caret — user can bold / change size without pre-selecting text).
- **Font + size controls** use toolbar **buttons**, not a native `<select>`, so `mousedown` can `preventDefault()` and keep the text field focused while formatting applies.
- **Inline styling** uses `_applyInlineStyle()` to wrap the current selection (or insert a styled zero-width span at a collapsed caret). `_applyFontFamily()` writes `font-family: var(--font-body|--font-display)`.
- **Font size** uses **A− / A+** step buttons (not S/M/L presets). Each click reads `parseFloat(getComputedStyle(textEl).fontSize)`, adds ±1 px, and writes back as `textEl.style.fontSize = Math.max(8, cur ± 1) + 'px'` — applied to the whole `.slide-object-text` element, not the selection. Undo/redo the `style.fontSize` change, not innerHTML.
- **Bold / italic** state: toggle `.is-active` via `document.queryCommandState(...)` on `selectionchange` / after commands.
- **Focus handoff:** `focusout` should not commit/close editing when focus moves into `#rteToolbar`; check `activeElement` / `relatedTarget` against the toolbar before setting `contenteditable="false"`.

## Keyboard & interaction summary

| Action | Binding |
|--------|---------|
| Toggle edit mode | `E` (not while typing in `contenteditable`), or hotzone / **Edit** button |
| Exit edit mode | **Done** in `#deckEditChrome` (top-left, hover-revealed), **Esc** (first Esc blurs focused text; Esc again exits), or **E** to toggle off |
| Multi-select toggle | `Ctrl` + click object (macOS: **Control** key, not Cmd) |
| Single select | Click object without Ctrl |
| Clear selection | Click slide background (empty area) |
| Undo / Redo | **Buttons** in `#deckEditChrome` (hover top-left cluster); or `Ctrl+Z` / **`Ctrl+Y` or `Ctrl+Shift+Z`** when edit mode and not typing in `contenteditable`; macOS **`Cmd+Z`**, **`Cmd+Shift+Z`**, **`Cmd+Y`** |
| Save | **Save** button in `#deckLeftHover` (row with Edit/Pages, edit mode only, hover-revealed) or `Ctrl+S` / **Cmd+S** |
| Bold / italic / font / size | Floating `#rteToolbar` when text is focused |
| Save to localStorage | `Ctrl+S` saves the full `.slides-offset` structure, not just per-slide inner HTML |
| Export HTML | Sidebar button; strips edit-mode / selected-state classes; produces self-contained responsive file |
| Export PDF | Sidebar button → ratio picker (16:9 / 4:3) → builds a fresh fixed-px HTML, opens in new tab, auto-prints; **never** uses CSS transform scaling — see §Export PDF |
| Add image | **＋ Image** button in sidebar (edit mode) → file picker → creates graphic slide object on current slide |
| Replace image | **Double-click** any `[data-object-type="graphic"]` slide object → file picker → replaces `<img>` src; supports undo |
| Replace slide background | `.slide-bg-replace-btn[data-bg-target="<CSS selector>"]` button → file picker → sets `style.backgroundImage` on target element; supports undo |

## Export PDF (fixed-px content injection)

**Never use CSS `transform: scale()` for PDF export.** Browsers capture a pixel-exact screenshot at print time; scaling a viewport-unit layout down to the target page size produces blurry, color-degraded output identical to a low-resolution screenshot.

### Universal approach: CSS override (copy from reference; works for any deck)

This is the implementation in `examples/editable-deck-reference.html`. Use it by default — it requires no knowledge of per-deck content structure.

**How it works:** clones the live DOM, strips UI chrome via CSS `display:none!important`, overrides `html`/`body`/`.slide` to fixed `1280×720px`, injects `@page{size:1280px 720px;margin:0}`, removes `<script>` tags, inserts an auto-print script, then opens via Blob URL. Because the page renders at exactly 1280×720 with no `transform`, viewport-unit values (`clamp()`, `vw`, `vh`) resolve correctly at print time — no scaling, no quality loss.

```javascript
function exportPdf() {
  var PW = 1280, PH = 720;
  var clone = document.documentElement.cloneNode(true);
  sanitizeExportDocument(clone);          // strip edit-mode classes + chrome state
  clone.querySelectorAll('script').forEach(function(s) { s.remove(); });

  var style = document.createElement('style');
  style.textContent = [
    '@page{size:' + PW + 'px ' + PH + 'px;margin:0}',
    '*,*::before,*::after{animation:none!important;transition:none!important}',
    'html{scroll-snap-type:none!important;scroll-behavior:auto!important}',
    'html,body{width:' + PW + 'px!important;height:auto!important;overflow:visible!important}',
    '.slides-offset{display:block!important;width:' + PW + 'px!important}',
    '.slide{width:' + PW + 'px!important;height:' + PH + 'px!important;max-height:' + PH + 'px!important;' +
      'overflow:hidden!important;page-break-after:always!important;break-after:page!important}',
    '.slide:last-child{page-break-after:avoid!important;break-after:avoid!important}',
    '.progress-bar,.nav-dots,.deck-left-hover-anchor,.slide-sidebar,.rte-toolbar,' +
      '.slide-bg-replace-anchor,.slide-object-move,.slide-object-resize{display:none!important}',
    '.reveal{opacity:1!important;transform:none!important}'
  ].join('\n');
  clone.querySelector('head').appendChild(style);

  var ps = document.createElement('script');
  ps.textContent = 'document.fonts.ready.then(function(){setTimeout(function(){window.focus();window.print();},350);});';
  clone.querySelector('body').appendChild(ps);

  var blob = new Blob(['<!DOCTYPE html>\n' + clone.outerHTML], {type:'text/html;charset=utf-8'});
  var url = URL.createObjectURL(blob);
  var win = window.open(url, '_blank');
  if (!win) { URL.revokeObjectURL(url); alert('Allow popups then retry.'); return; }
  setTimeout(function(){ URL.revokeObjectURL(url); }, 60000);
}
```

Wire the button: `document.getElementById('btnExportPdf').addEventListener('click', exportPdf);`

**When to use the advanced approach below instead:** only when you need per-element pixel-perfect control (e.g., a split-panel layout where column widths must be exact fractions independent of viewport math). For most generated decks the universal approach above is sufficient.

### Advanced approach: build a fresh fixed-px HTML at target resolution

1. **Define a baseline layout** at a convenient fixed resolution (e.g. 1200×750 for 8:5, which maps cleanly to 16:9 and 4:3). This baseline has its own CSS with all sizes in plain `px` — no `clamp()`, no `vw`/`vh`.

2. **Extract current content from the live DOM** via `[data-oid]` selectors:
   ```javascript
   function txt(oid) {
     var el = document.querySelector('[data-oid="' + oid + '"] .slide-object-text');
     return el ? el.innerHTML : '';
   }
   // Background image: prefer inline style (user-replaced), then computed CSS
   var bgEl = document.querySelector('.left-bg');
   var bgImage = (bgEl && bgEl.style.backgroundImage && bgEl.style.backgroundImage !== 'none')
     ? bgEl.style.backgroundImage
     : (bgEl ? getComputedStyle(bgEl).backgroundImage : 'none');
   // Logo / other image elements
   var logoSrc = document.querySelector('img.logo-static').src;
   ```

3. **Scale baseline px values to target dimensions** (W×H chosen by user — e.g. 1920×1080 for 16:9):
   ```javascript
   var BW = 1200, BH = 750;
   var sx = W / BW, sy = H / BH, s = (sx + sy) / 2; // s for fonts/radii
   function px(v) { return Math.round(v) + 'px'; }
   // Example:
   // '.bm-n { font-size:' + px(24*s) + '; }'
   // '.page { grid-template-columns:' + px(460*sx) + ' 1fr; }'
   ```

4. **Assemble a self-contained print HTML** with the scaled CSS and injected content, then open via Blob URL:
   ```javascript
   var printHTML = '<!DOCTYPE html>...<style>' + css + '</style>...'
     + '<div class="page"><div class="left">...</div><div class="right">...</div></div>'
     + '<script>document.fonts.ready.then(function() {'
     + '  setTimeout(function() { window.print(); }, 500);'
     + '});<\/script>';
   var blob = new Blob([printHTML], { type: 'text/html; charset=utf-8' });
   window.open(URL.createObjectURL(blob), '_blank');
   ```
   The `@page { size: Wpx Hpx; margin: 0; }` rule in the print CSS makes the browser produce a PDF of exactly that size, natively rendered — no scaling, no quality loss.

### Design of the baseline CSS

The baseline CSS duplicates the visual design of the editable deck (same fonts, colors, layout proportions) but uses **only fixed `px` values**. Key mapping:

| Editable deck (viewport-unit CSS) | Baseline print CSS |
|---|---|
| `clamp(8px, 0.83vw, 10px)` | `px(10 * s)` |
| `clamp(20px, 2.67vw, 36px)` | `px(32 * s)` |
| `38.33%` left column | `px(460 * sx)` column |
| `grid-template-columns: 38.33% 1fr` | `grid-template-columns: ${px(460*sx)} 1fr` |

This is the **only** path that preserves backgrounds, gradients, custom fonts, and colors in print output across browsers.

### Multi-slide PDF (looping through deck slides)

For decks with more than one slide, iterate the live DOM slides and build one `.page` div per slide. Each page gets `page-break-after: always` (except the last) so the browser paginates correctly.

```javascript
// Collect real slides (NOT sidebar thumbnail clones)
var deckRoot = document.querySelector('.slides-offset');
var slides = Array.from(deckRoot.querySelectorAll(':scope > section.slide'));

// Helper: extract inline or computed background-image from an element
function bgImage(sel) {
  var el = document.querySelector(sel);
  if (!el) return 'none';
  return (el.style.backgroundImage && el.style.backgroundImage !== 'none')
    ? el.style.backgroundImage
    : getComputedStyle(el).backgroundImage;
}

// Helper: get text content of a data-oid object
function txt(oid) {
  var el = document.querySelector('[data-oid="' + oid + '"] .slide-object-text');
  return el ? el.innerHTML : '';
}

// Build one page HTML string per slide
var pages = slides.map(function(slide, i) {
  var slideId = slide.id; // e.g. "slide-0"
  // Extract objects from this slide by scoping selectors to slideId
  var h1El = slide.querySelector('[data-oid] .slide-object-text');
  // Or use OID-based helpers scoped to this slide's known OID prefix (e.g. "s" + i + "-")
  var bg = (slide.querySelector('.slide-bg') && slide.querySelector('.slide-bg').style.backgroundImage)
    || getComputedStyle(slide).backgroundImage || 'none';

  return '<div class="page" style="' + (i < slides.length - 1 ? 'page-break-after:always;' : '') + '">'
    + '<!-- slide ' + (i+1) + ' content -->'
    + '</div>';
});

var printHTML = '<!DOCTYPE html><html><head>'
  + '<style>'
  + '@media print { @page { size: ' + W + 'px ' + H + 'px; margin: 0; } body { margin: 0; } }'
  + '.page { width:' + px(BW*sx) + '; height:' + px(BH*sy) + '; position:relative; overflow:hidden; }'
  + '/* ... rest of fixed-px CSS ... */'
  + '</style></head><body>'
  + pages.join('')
  + '<script>document.fonts.ready.then(function(){ setTimeout(function(){ window.print(); }, 500); });<\/script>'
  + '</body></html>';

var blob = new Blob([printHTML], { type: 'text/html; charset=utf-8' });
window.open(URL.createObjectURL(blob), '_blank');
```

**OID namespacing for multi-slide:** When generating a multi-slide deck, prefix each slide's object OIDs with the slide index (e.g. `s0-title`, `s1-title`, `s2-title`). The PDF builder can then extract per-slide content by scoping `querySelector` to the slide element or by pattern-matching OIDs to the slide index.

**Background images per slide:** Each slide may have its own background element. Extract it by querying within the slide node:
```javascript
slides.forEach(function(slide, i) {
  var bgEl = slide.querySelector('[data-bg-target], .slide-bg, .left-bg');
  var bg = bgEl
    ? ((bgEl.style.backgroundImage && bgEl.style.backgroundImage !== 'none')
        ? bgEl.style.backgroundImage
        : getComputedStyle(bgEl).backgroundImage)
    : 'none';
  // Use `bg` in this slide's fixed-px CSS
});
```

## Text editing `focusout` / history

- Commit text to history when the user **leaves** the `contenteditable` field (deferred `setTimeout(0)` so `relatedTarget` / `activeElement` settle).
- RTE toolbar uses **`mousedown` preventDefault** to reduce spurious blur before formatting clicks.

## Generator checklist (Phase 3)

1. Every slide has unique `id="slide-N"`.
2. Movable content sits in `.slide-edit-layer` as `.slide-object` with unique `data-oid`.
3. Text objects: `.slide-object-move` + `.slide-object-resize` + `.slide-object-text` with `contenteditable="false"` until focused.
4. Include full `viewport-base.css` in `<style>`.
5. Define **slide theme** and **`--deck-chrome-*`** on `:root`; chrome CSS uses variables only.
6. Copy **deck runtime** from `examples/editable-deck-reference.html` (CSS + JS) or inline equivalent — keep `STORAGE_KEY` / deck id meta consistent if user needs multiple files.
7. After generating, verify at 1280×720: no slide overflow, handles visible only in edit mode.
8. Include `<input type="file" id="deckImgInput" accept="image/*" style="display:none">` and `<input type="file" id="deckBgInput" accept="image/*" style="display:none">` in the `<body>` for image upload features.
9. For any slide that has a replaceable background element, add `<div class="slide-bg-replace-anchor"><button class="slide-bg-replace-btn" data-bg-target="#your-bg-element-id">📷 Replace background</button></div>` inside the slide.
10. **Export PDF button** (`#btnExportPdf`) in the sidebar: implement using the fixed-px content injection approach (§Export PDF), **not** CSS `transform: scale()`. Write a baseline CSS that mirrors the deck's visual design in fixed px, extract content via `[data-oid]` selectors, scale by `W/BW` and `H/BH`, and open via Blob URL with `@page { size: Wpx Hpx; margin: 0; }` + `document.fonts.ready` auto-print.

## Files

| File | Role |
|------|------|
| [examples/editable-deck-reference.html](examples/editable-deck-reference.html) | Single-file working reference |
| [html-template.md](html-template.md) | Architecture notes + link to reference |
| [viewport-base.css](viewport-base.css) | Mandatory slide sizing |
