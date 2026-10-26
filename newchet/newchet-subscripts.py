r"""Make newchet-stix2-mathit{,-bold}.{tfm,vf}: the math italic of the stix2 package with subscripts closer to the letter.

TeX attaches a subscript at the width of a letter.  It attaches a superscript at the width plus the italic correction.  In
the Type 1 metrics of the stix2 package, the width of most italic capitals includes nearly all of their overhang.  For V,
the width is 0.696 em and the italic correction 0.045 em.  Subscripts then sit beyond the top-right corner of V, W, Y, T,
F, P and similar letters, far from their foot.

The virtual fonts written here draw the same STIX Two glyphs at the same places.  They change only where subscripts
attach.  A letter with a positive shift d gets a width smaller by d and an italic correction larger by d.  Width plus
italic correction stays the same.  So letters without a subscript, superscripts, primes and accents keep their places, to
within 2 sp of rounding.  Limits are the exception.  TeX offsets them by half the italic correction, so the label of
\stackrel{*}{T} and the limits of \mathop{T}\limits move by d/2.

d comes from the math italic of SticksToo (ntxstx2mi and ntxstx2bmi), Michael Sharpe's reworking of STIX Two.  It has the
same outlines, with metrics tuned for TeX's subscript placement.  d is measured from the glyph outline, since the side
bearings of a few letters differ between the two fonts.  Only positive d is used, so no subscript moves away from its
letter.  Regular a and g keep the metrics of stix2 (SKIP below).  The stix2 package sets subscripts 0.06 em lower than
SticksToo, so with the d of SticksToo they would almost touch the tail of a.  The g of SticksToo has a different outline,
so the comparison does not apply to it.

Usage: python3 newchet-subscripts.py, or make newchet-fonts in the chet repository.  It writes the four files into the
folder of this script.  It needs Python 3.7 or later, kpsewhich, tftopl, vptovf and t1disasm.  It also needs the TeX Live
packages stix2-type1 and stickstoo.  newchet.sty uses the fonts with its stix2 option when it finds them.
"""
import os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = [  # (stix2 tfm, reference tfm, stix2 pfb, reference pfb, first glyph of A-Z, first of a-z, output name)
    ('stix2-mathit', 'ntxstx2mi', 'STIX2Math.pfb', 'stickstooMath-Italic.pfb', 0x1D434, 0x1D44E, 'newchet-stix2-mathit'),
    ('stix2-mathit-bold', 'ntxstx2bmi', 'STIX2Math.pfb', 'stickstooMath-BoldItalic.pfb', 0x1D468, 0x1D482,
     'newchet-stix2-mathit-bold'),
]
# Letters that keep the metrics of stix2 (see the docstring)
SKIP = {'newchet-stix2-mathit': 'ag'}


def run(*args, **kw):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kw).stdout


def kpse(name):
    return run('kpsewhich', name).strip()


def stix2_version():
    """Date and version of the stix2 package whose metrics the fonts copy, e.g. 2021/01/14 v2.0.2-latex."""
    m = re.search(r'\\ProvidesPackage\{stix2\}\[(\S+ \S+)', open(kpse('stix2.sty')).read())
    return m.group(1) if m else 'unknown version'


def pl_of(tfm):
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, 'f.pl')
        run('tftopl', kpse(tfm + '.tfm'), out)
        return open(out).read()


def metrics(pl):
    """Width and italic correction of every character, keyed by the character code."""
    out = {}
    for m in re.finditer(r'^\(CHARACTER (C \S|O \d+)\n(.*?)\n   \)', pl, re.S | re.M):
        body = m.group(2)
        wd = re.search(r'\(CHARWD R (-?[\d.]+)\)', body)
        ic = re.search(r'\(CHARIC R (-?[\d.]+)\)', body)
        out[code(m.group(1))] = (float(wd.group(1)) if wd else 0.0, float(ic.group(1)) if ic else 0.0)
    return out


def code(tok):
    kind, val = tok.split()
    return ord(val) if kind == 'C' else int(val, 8)


def side_bearings(pfb):
    """Left side bearing of every glyph of a Type 1 font, in font units, keyed by glyph name."""
    text = run('t1disasm', kpse(pfb))
    out, cur = {}, None
    for line in text.split('\n'):
        m = re.match(r'^/([A-Za-z0-9_.]+) \{$', line)
        if m:
            cur = m.group(1)
        elif cur and line.strip().endswith('hsbw'):
            out[cur] = int(line.split()[0])
            cur = None
    return out


def glyph(first_capital, first_small, ch):
    """Unicode glyph name of a math italic letter; italic small h is U+210E."""
    cp = (first_capital + ord(ch) - 65) if ch.isupper() else (first_small + ord(ch) - 97)
    return 'uni210E' if cp == 0x1D455 else 'u%X' % cp


def build(base, ref, base_pfb, ref_pfb, cap, small, name):
    pl = pl_of(base)
    mb, mr = metrics(pl), metrics(pl_of(ref))
    lb, lr = side_bearings(base_pfb), side_bearings(ref_pfb)
    shift = {}
    for ch in [chr(c) for c in range(65, 91)] + [chr(c) for c in range(97, 123)]:
        g = glyph(cap, small, ch)
        (wb, _), (wr, _) = mb[ord(ch)], mr[ord(ch)]
        d = round((wb - lb[g] / 1000) - (wr - lr[g] / 1000), 4)
        if d > 0.0005 and ch not in SKIP.get(name, ''):
            shift[ord(ch)] = d
    checksum = re.search(r'\(CHECKSUM (O \d+)\)', pl).group(1)
    vpl = re.sub(r'\(CHECKSUM O \d+\)\n', '', pl)
    head = '(VTITLE %s: %s of stix2 %s, with subscripts closer to the letter)\n' % (name, base, stix2_version())
    mapfont = '(MAPFONT D 0\n   (FONTNAME %s)\n   (FONTCHECKSUM %s)\n   (FONTAT R 1.0)\n   (FONTDSIZE R 10.0)\n   )\n' % (
        base, checksum)
    vpl = head + vpl.replace('(LIGTABLE', mapfont + '(LIGTABLE', 1)

    def char(m):
        tok, body = m.group(1), m.group(2)
        c = code(tok)
        setchar = '(SETCHAR %s)' % tok
        if c in shift:
            d = shift[c]
            wd, ic = mb[c]
            body = re.sub(r'\(CHARWD R -?[\d.]+\)', '(CHARWD R %.4f)' % (wd - d), body)
            if '(CHARIC' in body:
                body = re.sub(r'\(CHARIC R -?[\d.]+\)', '(CHARIC R %.4f)' % (ic + d), body)
            else:
                body += '\n   (CHARIC R %.4f)' % (ic + d)
            setchar += ' (MOVERIGHT R -%.4f)' % d
        return '(CHARACTER %s\n%s\n   (MAP %s)\n   )' % (tok, body, setchar)

    vpl = re.sub(r'^\(CHARACTER (C \S|O \d+)\n(.*?)\n   \)', char, vpl, flags=re.S | re.M)
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, name + '.vpl')
        open(src, 'w').write(vpl)
        run('vptovf', src, os.path.join(HERE, name + '.vf'), os.path.join(HERE, name + '.tfm'))
    print('%s: subscript shifts (em) %s' % (name, ' '.join('%s %.3f' % (chr(c), d) for c, d in sorted(shift.items()))))


for f in FONTS:
    build(*f)
