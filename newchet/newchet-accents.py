r"""Make the virtual font newchet-stix2-mathsfit.{tfm,vf}: the regular sans-serif italic math font of the stix2 package,
with accents centred over the letters.

TeX centres an accent over a single letter at half of the letter's width plus italic correction.  It then moves the
accent right by the kern of the letter with the skew character of its font, character 127 in the stix2 fonts.  In
stix2-mathsfit, the font of \mathsfit, these kerns are too large.  An accent sits 0.100 em to the right of the top of
its letter, in the median over the 52 Latin letters, and 0.162 em for G.  So the hat of \hat{\mathsfit{G}} sits near the
right edge of G.  The bold font stix2-mathsfit-bold and the upright fonts stix2-mathsf and stix2-mathsf-bold are sound.

The virtual font written here draws the same STIX Two glyphs at the same places, with the same widths, heights, depths
and italic corrections.  It changes only the 54 kerns with the skew character: those of the 52 Latin letters and of the
dotless i and j.  The font has no other kerns and no ligatures.  So only accents move.  Letters, subscripts and
superscripts keep their places, and so do the arrows that the stix2 package takes from this font.

The kerns below come from newchet-accents-measure.py.  It renders each letter of stix2-mathsfit and of
stix2-mathsfit-bold.  It gives the regular letter the kern that puts its accent where the bold letter has it, measured
from the centre of the top of the ink.  The median distance from that centre is then 0.017 em, as in the bold font.

Usage: python3 newchet-accents.py, or make newchet-fonts in the chet repository.  It writes the two files into the
folder of this script.  It needs Python 3.7 or later, kpsewhich, tftopl and vptovf, and the TeX Live package stix2-type1.
newchet.sty uses the font with its stix2 option when it finds it.
"""
import os, re, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BASE, NAME = 'stix2-mathsfit', 'newchet-stix2-mathsfit'
SKEWCHAR = 0o177

# Kerns with the skew character in em, from newchet-accents-measure.py
# accent position right of the centre of the top, median over the 52 Latin letters: 0.100 em in stix2-mathsfit,
# 0.017 em in stix2-mathsfit-bold, and so in stix2-mathsfit with the kerns below
SANS_ITALIC = {'A': 0.146, 'B': 0.079, 'C': 0.080, 'D': 0.065, 'E': 0.064, 'F': 0.069, 'G': 0.074, 'H': 0.049, 'I': 0.054, 'J': 0.128, 'K': 0.054, 'L': -0.049, 'M': 0.053, 'N': 0.111, 'O': 0.067, 'P': 0.064, 'Q': 0.081, 'R': 0.075, 'S': 0.060, 'T': 0.036, 'U': 0.069, 'V': 0.036, 'W': 0.039, 'X': 0.061, 'Y': 0.032, 'Z': 0.072, 'a': 0.069, 'b': 0.074, 'c': 0.032, 'd': 0.091, 'e': 0.062, 'f': 0.054, 'g': -0.002, 'h': 0.078, 'i': 0.066, 'j': 0.068, 'k': 0.061, 'l': 0.059, 'm': 0.098, 'n': 0.082, 'o': 0.059, 'p': 0.087, 'q': 0.062, 'r': 0.063, 's': 0.023, 't': 0.006, 'u': 0.064, 'v': 0.015, 'w': 0.033, 'x': 0.058, 'y': 0.033, 'z': 0.043, 'imath': 0.068, 'jmath': 0.081}

# Slots of stix2-mathsfit: Latin letters at their ASCII codes, then the dotless i and j
SLOTS = {'imath': 0x7B, 'jmath': 0x7C}


def run(*args, **kw):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kw).stdout


def kpse(name):
    return run('kpsewhich', name).strip()


def stix2_version():
    """Date and version of the stix2 package whose metrics the font copies, e.g. 2021/01/14 v2.0.2-latex."""
    m = re.search(r'\\ProvidesPackage\{stix2\}\[(\S+ \S+)', open(kpse('stix2.sty')).read())
    return m.group(1) if m else 'unknown version'


def pl_of(tfm):
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, 'f.pl')
        run('tftopl', kpse(tfm + '.tfm'), out)
        return open(out).read()


def code(tok):
    kind, val = tok.split()
    return ord(val) if kind == 'C' else int(val, 8)


def tok(c):
    return 'C %s' % chr(c) if chr(c).isalnum() else 'O %o' % c


def slot(name):
    return SLOTS[name] if name in SLOTS else ord(name)


def build(base, table, name):
    """Write name.vf and name.tfm: the font base, with the kerns of the characters in table with the skew character
    replaced by the amounts given in em."""
    kern = {slot(n): k for n, k in table.items()}
    pl = pl_of(base)
    # The kerning program of the base font must hold kerns with the skew character and nothing else
    ligtable = re.search(r'^\(LIGTABLE\n(.*?)\n   \)\n', pl, re.S | re.M)
    labels, old = [], {}
    for line in ligtable.group(1).splitlines():
        label = re.fullmatch(r'\s*\(LABEL (C \S|O \d+)\)', line)
        krn = re.fullmatch(r'\s*\(KRN O %o R (-?[\d.]+)\)' % SKEWCHAR, line)
        assert label or krn or line.strip() == '(STOP)', '%s: unexpected %s' % (base, line.strip())
        if label:
            labels.append(code(label.group(1)))
        elif krn:
            old.update({c: float(krn.group(1)) for c in labels})
        else:
            labels = []
    assert set(old) == set(kern), '%s: the characters with a kern differ from those of the table' % base
    new = '\n'.join('   (LABEL %s)\n   (KRN O %o R %.4f)\n   (STOP)' % (tok(c), SKEWCHAR, kern[c]) for c in sorted(kern))
    checksum = re.search(r'\(CHECKSUM (O \d+)\)', pl).group(1)
    vpl = re.sub(r'\(CHECKSUM O \d+\)\n', '', pl)
    head = '(VTITLE %s: %s of stix2 %s, with accents centred over the letters)\n' % (name, base, stix2_version())
    mapfont = '(MAPFONT D 0\n   (FONTNAME %s)\n   (FONTCHECKSUM %s)\n   (FONTAT R 1.0)\n   (FONTDSIZE R 10.0)\n   )\n' % (
        base, checksum)
    vpl = head + vpl.replace(ligtable.group(0), mapfont + '(LIGTABLE\n' + new + '\n   )\n', 1)
    # tftopl repeats the kerns of each character in a comment, which would now be out of date
    vpl = re.sub(r'\n   \(COMMENT\n      \(KRN .*?\n      \)', '', vpl, flags=re.S)
    vpl = re.sub(r'^\(CHARACTER (C \S|O \d+)\n(.*?)\n   \)',
                 lambda m: '(CHARACTER %s\n%s\n   (MAP (SETCHAR %s))\n   )' % (m.group(1), m.group(2), m.group(1)),
                 vpl, flags=re.S | re.M)
    with tempfile.TemporaryDirectory() as d:
        src = os.path.join(d, name + '.vpl')
        open(src, 'w').write(vpl)
        run('vptovf', src, os.path.join(HERE, name + '.vf'), os.path.join(HERE, name + '.tfm'))
    left = sorted((old[slot(n)] - k, n) for n, k in table.items())
    print('%s: accents move left by %.3f em in the median, and most for %s, by %.3f em'
          % (name, left[len(left) // 2][0], left[-1][1], left[-1][0]))


build(BASE, SANS_ITALIC, NAME)
