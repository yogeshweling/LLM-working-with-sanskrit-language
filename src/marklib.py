"""Classifier for the three marking rules: Mahaprana, Samyuktakshara, Dirgha Samyukta."""
import re, html

ASP = set('खघछझठढथधफभ')
USH = set('षह')
LONG_MATRA = set('ाीूॄॣेैोौ')
LONG_INDEP = set('आईऊॠएऐओऔॐ')
TRANSPARENT = set(' -ऽ‌‍')

TOKEN = re.compile(
    r'(?P<v>[अआइईउऊऋॠएऐओऔॐ][ंँः]*)'
    r'|(?P<a>(?:[क-ह]्)*[क-ह](?!्)[ािीुूृॄॢॣेैोौ]*[ंँः]*)'
    r'|(?P<h>(?:[क-ह]्)+)'
    r'|(?P<o>.)', re.S)

counts = {'mp': 0, 'sy': 0, 'dg': 0, 'total': 0}


def tokenise(s):
    toks = []
    for m in TOKEN.finditer(s):
        kind = m.lastgroup
        t = m.group(0)
        cons = [c for c in t if 'क' <= c <= 'ह']
        toks.append({'k': kind, 't': t, 'cons': cons})
    return toks


def conjunct_follows(toks, i):
    tot = 0
    j = i + 1
    n = len(toks)
    while j < n:
        tk = toks[j]
        if tk['k'] == 'o' and tk['t'] in TRANSPARENT:
            j += 1
            continue
        if tk['k'] == 'h':
            tot += len(tk['cons'])
            j += 1
            continue
        if tk['k'] == 'a':
            tot += len(tk['cons'])
        break
    return tot >= 2


def is_long(tk):
    if tk['k'] == 'a':
        return any(c in LONG_MATRA for c in tk['t'])
    if tk['k'] == 'v':
        return tk['t'][0] in LONG_INDEP
    return False


def classify(s):
    toks = tokenise(s)
    for i, tk in enumerate(toks):
        cl = []
        if tk['k'] in ('a', 'h'):
            if tk['k'] == 'a':
                counts['total'] += 1
            if any(c in ASP or c in USH for c in tk['cons']):
                cl.append('mp'); counts['mp'] += 1
            if len(tk['cons']) >= 2:
                cl.append('sy'); counts['sy'] += 1
        if tk['k'] in ('a', 'v') and is_long(tk) and conjunct_follows(toks, i):
            cl.append('dg'); counts['dg'] += 1
        tk['cl'] = cl
    return toks


def mark_text(s):
    out = []
    for tk in classify(s):
        e = html.escape(tk['t'])
        if tk['cl']:
            out.append('<span class="%s">%s</span>' % (' '.join(tk['cl']), e))
        else:
            out.append(e)
    return ''.join(out)


def debug(s):
    return ''.join(('[%s:%s]' % (tk['t'], '+'.join(tk['cl'])) if tk['cl'] else tk['t']) for tk in classify(s))
