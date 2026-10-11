import re, html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marklib as M

DECODED, OUT_PDF = sys.argv[1], sys.argv[2]   # usage: make_pdf.py decoded.txt out.pdf
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(DECODED, encoding='utf-8').read().split('\n')
D = str.maketrans('०१२३४५६७८९', '0123456789')

def clean_head(l):
    l = l.strip()
    if l.startswith('. '):
        l = '॥ ' + l[2:]
    if l.endswith('.'):
        l = l[:-1] + ' ॥'
    return l

def line_html(s):
    return '<span class="ln">%s</span>' % M.mark_text(s)

i_dh = SRC.index('ध्यानम्')
i_start = next(i for i, l in enumerate(SRC) if l.startswith('. अथ'))
nyasa, dhyana, verses_raw = SRC[2:i_dh], SRC[i_dh + 1:i_start], SRC[i_start + 1:]
verses, colophon, k = [], [], 0
while k < len(verses_raw):
    l = verses_raw[k]
    if l.startswith('. इति'):
        colophon = verses_raw[k:]; break
    l2 = verses_raw[k + 1]
    m = re.search(r'\. ([०-९]+)\.$', l2)
    n = int(m.group(1).translate(D))
    a = re.sub(r',$', ' ।', l.strip())
    b = re.sub(r',? ?[०-९]+\.$', '', l2).strip().rstrip('.').rstrip(',').strip()
    verses.append((n, a, b + ' ॥ ' + m.group(1) + ' ॥'))
    k += 2
assert len(verses) == 183

P = []
P.append('<h2>प्रारम्भ</h2><p class="head">%s</p>' % M.mark_text(clean_head(SRC[0])))
P.append('<h3>न्यासः</h3><div class="lines">' + ''.join(line_html(l.strip()) for l in nyasa) + '</div>')
P.append('<h3>ध्यानम्</h3><div class="lines">' + ''.join(line_html(re.sub(r'\.$', ' ॥', l.strip())) for l in dhyana) + '</div>')
P.append('<h2>नामावलिः</h2><p class="head">%s</p><ol class="verses">' % M.mark_text(clean_head(SRC[i_start])))
for n, a, b in verses:
    P.append('<li id="v%d"><span class="no">%d</span><div class="vt">%s%s</div></li>' % (n, n, line_html(a), line_html(b)))
P.append('</ol><div class="lines colo">' + ''.join(line_html(clean_head(l)) for l in colophon) + '</div>')

tpl = open(os.path.join(HERE, 'print_template.html'), encoding='utf-8').read()
c = M.counts
tpl = tpl.replace('{{BODY}}', '\n'.join(P)).replace('{{MP}}', str(c['mp'])).replace('{{SY}}', str(c['sy'])).replace('{{DG}}', str(c['dg'])).replace('{{TOTAL}}', str(c['total']))
html_path = os.path.splitext(OUT_PDF)[0] + '.html'
open(html_path, 'w', encoding='utf-8').write(tpl)
print('counts:', c)

# Render the HTML to PDF with Chromium (Playwright). Needs: pip install playwright && playwright install chromium
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page()
    pg.goto('file://' + os.path.abspath(html_path))
    pg.pdf(path=OUT_PDF, format='A4', print_background=True, prefer_css_page_size=True,
           display_header_footer=True, header_template='<span></span>',
           footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#777"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
    br.close()
print('wrote', OUT_PDF)
