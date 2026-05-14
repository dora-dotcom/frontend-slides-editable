#!/usr/bin/env python3
"""Patch generated HTML decks to add PDF export button + function + self-check.

Uses plain str.replace / str.split instead of re.sub to avoid backslash
interpretation in replacement strings.
"""

from pathlib import Path

# ── HTML sidebar button ────────────────────────────────────────────────────────
PDF_BUTTON = '<button type="button" id="btnExportPdf" style="width:100%;">Export PDF</button>'

# ── JS function (inserted verbatim after exportHtml closes) ───────────────────
# Keep all JS escape sequences as plain text so no Python escape processing occurs.
EXPORT_PDF_FN = r"""
  function exportPdf() {
    const PW = 1280, PH = 720;
    const clone = document.documentElement.cloneNode(true);
    sanitizeExportDocument(clone);
    clone.querySelectorAll('script').forEach((s) => s.remove());

    const style = document.createElement('style');
    style.id = 'deck-print-override';
    style.textContent = [
      '@page{size:' + PW + 'px ' + PH + 'px;margin:0}',
      '*,*::before,*::after{animation:none!important;transition:none!important}',
      'html{scroll-snap-type:none!important;scroll-behavior:auto!important}',
      'html,body{width:' + PW + 'px!important;height:auto!important;overflow:visible!important;background:#000!important}',
      '.slides-offset{display:block!important;width:' + PW + 'px!important}',
      '.slide{' +
      '  width:' + PW + 'px!important;height:' + PH + 'px!important;' +
      '  max-height:' + PH + 'px!important;overflow:hidden!important;' +
      '  page-break-after:always!important;break-after:page!important;' +
      '  position:relative!important;display:flex!important;flex-direction:column!important' +
      '}',
      '.slide:last-child{page-break-after:avoid!important;break-after:avoid!important}',
      ['.progress-bar','.nav-dots','.deck-left-hover-anchor','#deckLeftHover',
       '.slide-sidebar','#slideSidebar','.rte-toolbar','#rteToolbar',
       '.slide-bg-replace-anchor','.slide-object-move','.slide-object-resize',
       '.snap-line-v','.snap-line-h'].join(',') + '{display:none!important}',
      '.reveal{opacity:1!important;transform:none!important}',
      '.slide-edit-layer{pointer-events:none!important}'
    ].join('\n');

    const head = clone.querySelector('head');
    if (head) head.appendChild(style);

    const printScript = document.createElement('script');
    printScript.textContent = [
      'document.fonts.ready',
      '  .then(function(){setTimeout(function(){window.focus();window.print();},350);})',
      '  .catch(function(){setTimeout(function(){window.focus();window.print();},900);});'
    ].join('');
    const body = clone.querySelector('body');
    if (body) body.appendChild(printScript);

    const html = '<!DOCTYPE html>\n' + clone.outerHTML;
    const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const win = window.open(url, '_blank');
    if (!win) {
      URL.revokeObjectURL(url);
      alert('PDF export blocked — please allow popups for this page, then try again.');
      return;
    }
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  }
"""

# ── Startup self-check (inserted before the final deck._updateChrome call) ────
SELF_CHECK = r"""
  // Startup self-check: warn if any critical runtime element is absent
  (['editToggle','pagesToggle','deckEditChrome','btnExport','btnExportPdf','rteToolbar','filmstripList'])
    .filter((id) => !document.getElementById(id))
    .forEach((id) => console.error('[deck-runtime] Missing required element: #' + id));
"""


def patch(path: Path) -> str:
    """Return one of: 'patched', 'skipped', 'no-runtime', or an error label."""
    text = path.read_text(encoding='utf-8')

    if 'SlideDeck' not in text and 'SlideObjectEditor' not in text:
        return 'no-runtime'
    if 'btnExportPdf' in text:
        return 'skipped'

    # ── 1. Insert PDF button after Export HTML button ──────────────────────────
    # Handles optional style attr variations across generated files
    ANCHORS_BTN = [
        '<button type="button" id="btnExport" style="width:100%;">Export HTML</button>',
        '<button type="button" id="btnExport">Export HTML</button>',
    ]
    for anchor in ANCHORS_BTN:
        if anchor in text:
            text = text.replace(anchor, anchor + '\n    ' + PDF_BUTTON, 1)
            break
    else:
        return 'no-export-btn'

    # ── 2. Insert exportPdf() right after exportHtml() closes ─────────────────
    END_MARKER = "URL.revokeObjectURL(a.href);\n  }"
    if END_MARKER not in text:
        return 'no-export-fn-end'
    text = text.replace(END_MARKER, END_MARKER + EXPORT_PDF_FN, 1)

    # ── 3. Wire up btnExportPdf listener after btnExport listener ─────────────
    LISTENER_ANCHOR = "document.getElementById('btnExport').addEventListener('click', exportHtml);"
    if LISTENER_ANCHOR not in text:
        return 'no-listener'
    text = text.replace(
        LISTENER_ANCHOR,
        LISTENER_ANCHOR + "\n  document.getElementById('btnExportPdf').addEventListener('click', exportPdf);",
        1
    )

    # ── 4. Self-check before the final deck._updateChrome(); })(); ────────────
    # Find the last occurrence of this pattern (end of IIFE)
    FINAL_MARKER = "\n  deck._updateChrome();\n})();"
    last_idx = text.rfind(FINAL_MARKER)
    if last_idx == -1:
        return 'no-final-chrome'
    text = text[:last_idx] + SELF_CHECK + text[last_idx:]

    path.write_text(text, encoding='utf-8')
    return 'patched'


def main():
    root = Path(__file__).parent.parent
    targets = [
        root / 'examples' / 'generated' / 'frontend-slides-editable-readme-demo.html',
        *sorted((root / 'examples' / 'generated' / 'presets').glob('*.html')),
        root / 'examples' / 'pitch-deck-readme-editable-fork.html',
    ]
    for p in targets:
        result = patch(p)
        print(f'  {result:20s}  {p.name}')


if __name__ == '__main__':
    main()
