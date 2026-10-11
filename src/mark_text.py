"""Mark any Unicode Devanagari text with the three rules (Mahaprana, Samyuktakshara, Dirgha Samyukta).

usage: python src/mark_text.py input.txt output.html [--pdf output.pdf]

One input line becomes one output line. The input must be Unicode Devanagari text
(for PDFs that use a legacy font, decode them first; see decode.py).
"""
import argparse, html, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marklib as M

CSS = """
body{font-family:'FreeSerif','Noto Serif Devanagari','Mangal',serif;margin:24px;color:#1b1a22;max-width:760px;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.legend{font-family:'FreeSans',sans-serif;font-size:11pt;display:flex;gap:18px;flex-wrap:wrap;align-items:center;margin-bottom:6px}
.sw{font-size:17pt;padding:0 3pt}
.note{font-family:'FreeSans',sans-serif;font-size:9.5pt;color:#555;margin:0 0 14px}
.ln{display:block;font-size:19pt;line-height:2}
.mp{color:#c2185b;font-weight:700}
.sy{background:#ffe45c;border-radius:2pt}
.dg{text-decoration:underline;text-decoration-color:#0f9d58;text-decoration-thickness:1.6pt;text-underline-offset:2.5pt;text-decoration-skip-ink:none}
"""
LEGEND = """<div class="legend">
<span><span class="sw mp">ख घ भ ष ह</span> Mahaprana</span>
<span><span class="sw sy">क्ष स्त</span> Samyuktakshara</span>
<span><span class="sw dg">दी</span><span class="sw sy">क्षा</span> Dirgha Samyukta (long letter just before a conjunct)</span>
</div>
<p class="note">Pink: ख घ छ झ ठ ढ थ ध फ भ plus ष ह (श स are not marked). Yellow: any conjunct. Green underline: the long-vowel letter immediately before a conjunct; reading is continuous across spaces and hyphens within a line.</p>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('input'); ap.add_argument('output'); ap.add_argument('--pdf')
    a = ap.parse_args()
    lines = open(a.input, encoding='utf-8').read().split('\n')
    body = '\n'.join('<span class="ln">%s</span>' % M.mark_text(l) for l in lines if l.strip())
    doc = '<meta charset="utf-8"><title>Marked text</title><style>%s</style>%s\n%s' % (CSS, LEGEND, body)
    open(a.output, 'w', encoding='utf-8').write(doc)
    print('counts:', M.counts)
    if a.pdf:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br = pw.chromium.launch(); pg = br.new_page()
            pg.goto('file://' + os.path.abspath(a.output))
            pg.pdf(path=a.pdf, format='A4', print_background=True)
            br.close()
        print('wrote', a.pdf)

if __name__ == '__main__':
    main()
