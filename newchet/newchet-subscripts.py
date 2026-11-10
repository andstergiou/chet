r"""Make the virtual fonts newchet-stix2-{mathit,mathit-bold,mathrm,mathrm-bold,mathcal}.{tfm,vf}: the math italic, upright
and calligraphic fonts of the stix2 package with subscripts closer to the letter.

TeX attaches a subscript at the width of a letter.  It attaches a superscript at the width plus the italic correction.  In
the Type 1 metrics of the stix2 package, the width of many letters includes nearly all of their overhang.  For italic V,
the width is 0.696 em and the italic correction 0.045 em.  Subscripts then sit beyond the top-right corner of V, W, Y, T,
F and P, beyond the arm of gamma, beyond the top of nabla and Gamma, and beyond the tail of calligraphic L.

The virtual fonts written here draw the same STIX Two glyphs at the same places.  They change only where subscripts
attach.  A letter with a shift d gets a width smaller by d and an italic correction larger by d.  Width plus italic
correction stays the same.  So letters without a subscript, superscripts, primes and accents keep their places, to within
2 sp of rounding.  Limits are the exception.  TeX offsets them by half the italic correction, so the label of
\stackrel{*}{T} and the limits of \mathop{T}\limits move by d/2.

The shifts below come from newchet-subscripts-measure.py, which sets every letter with 180 subscripts and measures the
ink.  The measure is the smallest horizontal distance between the ink of a letter and that of a subscript.  d brings the
subscripts a, n and i to the median distance of the italic lowercase letters, 0.127 em in regular and 0.116 em in bold.
d is smaller where one of the 180 subscripts would then come closer to the letter than it comes to any italic capital of
stix2.  That limit sets d for V and W and for gamma and nabla, by the ascender of b, k and l.  d below 0.005 em is left
out.  The calligraphic font has no bold, so newchet uses it in bold math too.

Usage: python3 newchet-subscripts.py, or make newchet-fonts in the chet repository.  It writes the ten files into the
folder of this script.  It needs Python 3.7 or later, kpsewhich, tftopl and vptovf, and the TeX Live package stix2-type1.
newchet.sty uses the fonts with its stix2 option when it finds them.
"""
import os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

# Subscript shifts in em, from newchet-subscripts-measure.py
# regular: target gap 0.127 em
ITALIC = {'C': 0.035, 'E': 0.011, 'F': 0.111, 'H': 0.055, 'I': 0.059, 'J': 0.107, 'M': 0.052, 'N': 0.106, 'O': 0.021, 'P': 0.147, 'S': 0.012, 'T': 0.201, 'U': 0.112, 'V': 0.247, 'W': 0.228, 'X': 0.049, 'Y': 0.234, 'Z': 0.013, 'f': 0.213, 'j': 0.049, 'r': 0.142, 't': 0.030, 'y': 0.021, 'beta': 0.005, 'gamma': 0.089, 'delta': 0.016, 'epsilon': 0.010, 'zeta': 0.057, 'theta': 0.022, 'nu': 0.013, 'xi': 0.018, 'pi': 0.052, 'sigma': 0.079, 'tau': 0.080, 'chi': 0.017, 'vartheta': 0.032, 'varpi': 0.078, 'varsigma': 0.026, 'partial': 0.021}
UPRIGHT = {'D': 0.010, 'F': 0.055, 'G': 0.014, 'J': 0.051, 'N': 0.041, 'O': 0.011, 'P': 0.131, 'T': 0.100, 'U': 0.058, 'V': 0.171, 'W': 0.149, 'Y': 0.115, 'r': 0.046, 'v': 0.070, 'w': 0.070, 'y': 0.071, 'Gamma': 0.183, 'Theta': 0.009, 'Upsilon': 0.115, 'Phi': 0.013, 'Psi': 0.083, 'nabla': 0.206}
CALLIGRAPHIC = {'B': 0.018, 'C': 0.041, 'D': 0.023, 'E': 0.030, 'F': 0.198, 'G': 0.012, 'H': 0.058, 'I': 0.051, 'J': 0.069, 'K': 0.019, 'L': 0.042, 'N': 0.216, 'O': 0.030, 'P': 0.117, 'T': 0.285, 'V': 0.102, 'W': 0.085, 'X': 0.043, 'Y': 0.028}
# bold: target gap 0.116 em
ITALIC_BOLD = {'B': 0.028, 'C': 0.037, 'D': 0.012, 'E': 0.009, 'F': 0.118, 'H': 0.060, 'I': 0.063, 'J': 0.124, 'M': 0.059, 'N': 0.105, 'O': 0.031, 'P': 0.109, 'S': 0.020, 'T': 0.205, 'U': 0.124, 'V': 0.268, 'W': 0.222, 'X': 0.038, 'Y': 0.221, 'Z': 0.030, 'b': 0.009, 'f': 0.230, 'g': 0.039, 'j': 0.020, 'r': 0.123, 't': 0.025, 'v': 0.010, 'w': 0.007, 'x': 0.013, 'y': 0.017, 'gamma': 0.063, 'pi': 0.006, 'sigma': 0.150, 'tau': 0.061, 'varpi': 0.092, 'varsigma': 0.008, 'partial': 0.006}
UPRIGHT_BOLD = {'D': 0.015, 'F': 0.076, 'J': 0.068, 'N': 0.042, 'O': 0.022, 'P': 0.089, 'T': 0.106, 'U': 0.084, 'V': 0.172, 'W': 0.147, 'Y': 0.119, 'r': 0.051, 'v': 0.086, 'w': 0.086, 'y': 0.079, 'Gamma': 0.190, 'Theta': 0.023, 'Upsilon': 0.097, 'Psi': 0.079, 'nabla': 0.136}

# Slots of the stix2 fonts: Latin letters at their ASCII codes, lowercase Greek and partial in the math italic, Greek
# capitals and nabla in the upright font
GREEK = ('alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi pi rho sigma tau upsilon phi chi psi '
         'omega varepsilon vartheta varpi varrho varsigma varphi').split()
CAPGREEK = 'Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega'.split()
SLOTS = {name: 0x0B + i for i, name in enumerate(GREEK)}
SLOTS.update({name: i for i, name in enumerate(CAPGREEK)})
SLOTS.update(partial=0x29, nabla=0x28)

FONTS = [  # (stix2 font, shifts, output name)
    ('stix2-mathit', ITALIC, 'newchet-stix2-mathit'),
    ('stix2-mathit-bold', ITALIC_BOLD, 'newchet-stix2-mathit-bold'),
    ('stix2-mathrm', UPRIGHT, 'newchet-stix2-mathrm'),
    ('stix2-mathrm-bold', UPRIGHT_BOLD, 'newchet-stix2-mathrm-bold'),
    ('stix2-mathcal', CALLIGRAPHIC, 'newchet-stix2-mathcal'),
]


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


def slot(name):
    return SLOTS[name] if name in SLOTS else ord(name)


def build(base, table, name):
    """Write name.vf and name.tfm: the font base, with the subscripts of the characters in table moved left by the
    amounts given in em."""
    shift = {slot(n): d for n, d in table.items()}
    pl = pl_of(base)
    assert '(LIGTABLE' in pl, base
    mb = metrics(pl)
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
    print('%s: subscript shifts (em) %s' % (name, ' '.join('%s %.3f' % (n, d) for n, d in table.items())))


for base, table, name in FONTS:
    build(base, table, name)
