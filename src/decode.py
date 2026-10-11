"""Glyph-to-Unicode decoder for the legacy font used in the source PDF (reverse-engineered; see README)."""
import re, sys, json

FULL = {
 'k':'क','o':'ख','g':'ग','"':'घ',"'":'ङ','c':'च','D':'छ','j':'ज','q':'ट','Q':'ठ','f':'ड','F':'ढ','[':'ण',
 't':'त','w':'थ','d':'द','x':'ध','n':'न','p':'प',')':'फ','b':'ब','É':'भ','m':'म','y':'य','r':'र','l':'ल',
 'v':'व','z':'श',';':'ष','s':'स','h':'ह',']':'क्ष','}':'ज्ञ',
 'ï':'श्र','ñ':'श्व','à':'प्र','ä':'ब्र','ü':'ह्म','ö':'स्र','ò':'ष्ट','ó':'ष्ठ','Ô':'द्र','Ö':'द्व','Ï':'द्ध',
 'Ì':'द्ग','Ú':'न्न','Ù':'न्त्र','Â':'ञ्च','Ã':'ञ्ज','Ä':'त्त','Ç':'त्र','³':'क्र','´':'क्त','¢':'ग्र','æ':'भ्र',
 'ì':'व्र','â':'ब्ज','þ':'ह्व','õ':'स्न','Æ':'त्न','¶':'ग्न','¹':'घ्न','¿':'ज्र','¬':'क्ल','±':'क्त्र','¾':'ज्ज',
 'Î':'द्द','Ñ':'द्भ','Ý':'प्त','ô':'स्त्र','ý':'ह्य','è':'म्र','Œ':'ङ्ख','Ó':'द्ब','ç':'म्न','í':'श्च','Š':'क्क',
 '“':'ङ्क्त','”':'ट्ट','½':'च्च','û':'ह्न','’':'ह्ल','‘':'ल्ल','ÿ':'ह्र','¼':'ङ्ग','»':'ङ्क','‹':'क्च',
 'Ê':'दु','Ë':'दू','é':'रु','ê':'रू','÷':'हु','ù':'हृ','†':'दृ','„':'क्लृ','ƒ':'',
}
# full glyphs that carry an implicit matra
IMPL = {'Ê':'ु','Ë':'ू','é':'ु','ê':'ू','÷':'ु','ù':'ृ','†':'ृ','„':'ृ'}
FULL['Ê']='द';FULL['Ë']='द';FULL['é']='र';FULL['ê']='र';FULL['÷']='ह';FULL['ù']='ह';FULL['†']='द';FULL['„']='क्ल'
del FULL['ƒ']
FULL['*']='द्य'; FULL['Ò']='द्म'
HALF = {'K':'क्','O':'ख्','G':'ग्','¸':'घ्','C':'च्','J':'ज्','Z':'श्','T':'त्','W':'थ्','N':'न्','P':'प्','B':'ब्',
        '_':'भ्','M':'म्','S':'स्','V':'व्','L':'ल्','X':'ध्','{':'ण्','ú':'क्ष्','®':'क्त्','Á':'ञ्','Å':'त्त्','È':'त्र्',
        'Þ':'प्त्',':':'ष्'}
POST = {'(':'्य','+':'्र'}
MATRA = {'a':'ा','I':'ी','u':'ु','U':'ू','e':'े','E':'ै','…':'ु','‚':'ु','ª':'ू','ƒ':'ू','&':'ृ','«':'ृ',
         '<':'ं','>':'ः','—':'ं'}
INDEP = {'A':'अ','#':'इ','%':'उ','@':'ए','\\':'ऋ','`':'ॐ'}
DIG = dict(zip('0123456789','०१२३४५६७८९'))
unmapped = {}

def decode_line(s):
    out=[]            # list of syllable dicts or literal strings
    i=0; n=len(s)
    pend_i=False
    parts=[]          # open cluster
    def flush_cluster(impl=''):
        pass
    while i<n:
        ch=s[i]
        if ch=='' or ch=='\x0c':
            i+=1; continue
        if ch in FULL or ch in HALF:
            # build cluster
            parts=[]
            while i<n and (s[i] in HALF or s[i] in FULL):
                g=s[i]
                if g in HALF:
                    parts.append(HALF[g]); i+=1; continue
                parts.append(FULL[g]); impl=IMPL.get(g,''); i+=1
                while i<n and s[i] in POST:
                    parts[-1]+=POST[s[i]]; i+=1
                if i<n and s[i] in ('œ','!'):
                    parts[-1]+='्'; i+=1
                    # cluster continues only if next is consonant glyph
                    if i<n and (s[i] in FULL or s[i] in HALF) :
                        continue
                    else:
                        # word-final virama consonant, syllable complete
                        out.append({'c':''.join(parts),'m':'','i':pend_i,'r':False,'halant':True}); pend_i=False; parts=None
                        break
                break
            if parts is None: continue
            # matras
            m=''
            m+=impl
            while i<n:
                g=s[i]
                if g=='a' and i+1<n and s[i+1]=='e': m+='ो'; i+=2; continue
                if g=='a' and i+1<n and s[i+1]=='E': m+='ौ'; i+=2; continue
                if g in MATRA: m+=MATRA[g]; i+=1; continue
                break
            out.append({'c':''.join(parts),'m':m,'i':pend_i,'r':False}); pend_i=False
            continue
        if ch=='i':
            pend_i=True; i+=1; continue
        if ch=='R':
            # reph on last syllable
            for o in reversed(out):
                if isinstance(o,dict):
                    o['r']=True; break
            i+=1; continue
        if ch in INDEP:
            v=INDEP[ch]; i+=1
            if ch=='A':
                if s[i:i+2]=='ae': v='ओ'; i+=2
                elif s[i:i+2]=='aE': v='औ'; i+=2
                elif s[i:i+1]=='a': v='आ'; i+=1
                elif s[i:i+1]=='E': v='ऐ'; i+=1
            elif ch=='#' and s[i:i+1]=='I': v='ई'; i+=1
            elif ch=='%' and s[i:i+1]=='U': v='ऊ'; i+=1
            # trailing visarga/anusvara handled as literal tokens below
            out.append(v); continue
        if ch in MATRA and ch in '<>—':
            out.append(MATRA[ch]); i+=1; continue
        if ch=='=': out.append('ऽ'); i+=1; continue
        if ch=='!' or ch=='œ': out.append('्'); i+=1; continue
        if ch in DIG: out.append(DIG[ch]); i+=1; continue
        if ch in ' -,.\n': out.append(ch); i+=1; continue
        unmapped[ch]=unmapped.get(ch,0)+1
        out.append('⟨'+ch+'⟩'); i+=1
    res=[]
    for o in out:
        if isinstance(o,str): res.append(o)
        else:
            c=o['c']; m=o['m']
            # i matra before other matras
            r='र्' if o['r'] else ''
            res.append(r+c+('ि' if o['i'] else '')+m)
    return ''.join(res)
