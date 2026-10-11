"""Decode the pdftotext output of the source PDF into Unicode Devanagari.

Fixes a few verses that pdftotext splits across lines, then runs decode_line on every line."""
import re
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decode import decode_line, unmapped
SRC_TXT, OUT_TXT = sys.argv[1], sys.argv[2]   # usage: build_text.py raw.txt decoded.txt
t=open(SRC_TXT,encoding='utf-8').read().replace('paQee','paQe')
t=re.sub(r'inmaeh\n\s+R a maehnaiznI,','inmaeRha maehnaiznI,',t)
t=re.sub(r'devz\n\s+e I d\{fnIitSwa','devezI d{fnIitSwa',t)
t=re.sub(r'svaep\n\s+R aix-ivinmuR´a','svaeRpaix-ivinmuR´a',t)
t=re.sub(r'ivñtaemo\n\s+u I,','ivñtaemuoI,',t)
t=t.replace('Ne Ô','eNÔ')
t=re.sub(r'svaEd\n\s+R n-','svaERdn-',t)
t=re.sub(r'svaep\n\s+R in;','svaeRpin;',t)
t=t.replace('AyaeinyaeiR ninlya','AyaeinyaeRininlya')
lines=[]
for ln in t.split('\n'):
    ln=ln.replace('\x0c','').replace('','').strip()
    if not ln or 'shönam StaeÇm! - ' in ln: continue
    lines.append(decode_line(ln))
open(OUT_TXT,'w',encoding='utf-8').write('\n'.join(lines))
print(unmapped,len(lines))
