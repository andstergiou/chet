r"""Measure where accents should sit on the sans-serif italic letters of the stix2 package, and print the kern table of
newchet-accents.py.

TeX centres an accent over a single letter at half of the letter's width plus italic correction.  It then moves the
accent right by the kern of the letter with the skew character of its font.  Call the result the accent position of the
letter.  In stix2-mathsfit, the regular sans-serif italic of \mathsfit, these kerns are too large.  The accent position
lies 0.100 em to the right of the top of the letter, in the median over the 52 Latin letters, and 0.162 em for G.  The
bold font stix2-mathsfit-bold is sound, with a median of 0.017 em.  So are the upright fonts stix2-mathsf and
stix2-mathsf-bold, with 0.003 em.  For comparison, the math italic stix2-mathit has 0.037 em.

The script sets each letter of the regular and of the bold font alone and renders it.  The top of a letter is its ink
within 0.07 em of its highest point.  The centre of the top is the midpoint between the left and right edges of that
ink.  Each regular letter gets the kern that puts its accent position as far from the centre of its top as the accent
position of the bold letter is from the centre of its top.  The two fonts are weights of one design, so this carries the
choices of STIX Two for each letter over to the regular weight.  They include accents that sit towards the bowl of b,
d, h and k, and not over the ascender.

The letters are the 52 Latin letters and the dotless i and j.  These are the 54 characters of stix2-mathsfit with a kern
against the skew character.  The font has no other kerns.

Usage: python3 newchet-accents-measure.py.  It needs pdflatex, kpsewhich and tftopl, the TeX Live package stix2-type1,
pdftoppm (poppler), and the Python packages numpy and Pillow.  It renders 108 small pages at 4800 dpi, one at a time,
deleting each image after use.  It takes a few seconds.  Paste its output over the table in newchet-accents.py.
"""
import os, re, subprocess, tempfile
from multiprocessing import Pool

import numpy as np
from PIL import Image

DPI = 4800
PT = 72.27 / DPI  # TeX points per pixel
SIZE = 10.0  # font size in pt, so one em
LEFT, TOP, DEPTH, WIDTH = 10.0, 16.0, 9.0, 40.0  # page geometry in pt: letter at LEFT, baseline TOP below the top
BAND = 0.07  # depth of the top of a letter, in em
SKEWCHAR = 0o177
REGULAR, BOLD = 'stix2-mathsfit', 'stix2-mathsfit-bold'
NAMES = {0x7B: 'imath', 0x7C: 'jmath'}  # the dotless i and j; the Latin letters sit at their ASCII codes


def run(*args, **kw):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kw).stdout


def code(tok):
    kind, val = tok.split()
    return ord(val) if kind == 'C' else int(val, 8)


def metrics(tfm):
    """Half of the width plus italic correction of every character, and the kern of every character that has one with
    the skew character.  Both in em, keyed by the character code."""
    pl = run('tftopl', run('kpsewhich', tfm + '.tfm').strip())
    half = {}
    for m in re.finditer(r'^\(CHARACTER (C \S|O \d+)\n(.*?)\n   \)', pl, re.S | re.M):
        wd = re.search(r'\(CHARWD R (-?[\d.]+)\)', m.group(2))
        ic = re.search(r'\(CHARIC R (-?[\d.]+)\)', m.group(2))
        half[code(m.group(1))] = ((float(wd.group(1)) if wd else 0.0) + (float(ic.group(1)) if ic else 0.0)) / 2
    kern, labels = {}, []
    for line in pl[pl.index('(LIGTABLE'):pl.index('(CHARACTER')].splitlines():
        label = re.match(r'\s*\(LABEL (C \S|O \d+)\)', line)
        krn = re.match(r'\s*\(KRN (C \S|O \d+) R (-?[\d.]+)\)', line)
        if label:
            labels.append(code(label.group(1)))
        elif krn and code(krn.group(1)) == SKEWCHAR:
            kern.update({c: float(krn.group(2)) for c in labels})
        elif '(STOP)' in line:
            labels = []
    return half, kern


def document(slots):
    """The TeX source and the list of pages.  Each page sets one character alone, at LEFT, in the font at SIZE."""
    lines = [r'\documentclass{article}',
             r'\newcommand\pg[1]{\shipout\hbox{\vrule height %gpt depth %gpt width 0pt\kern%gpt #1}}' % (TOP, DEPTH, LEFT),
             r'\begin{document}',
             r'\pdfpagewidth=%gpt \pdfpageheight=%gpt \pdfhorigin=0pt \pdfvorigin=0pt' % (WIDTH, TOP + DEPTH)]
    pages = []
    for font in (REGULAR, BOLD):
        lines.append(r'\font\f=%s at %gpt' % (font, SIZE))
        for c in slots:
            lines.append(r'\pg{\f\char%d}' % c)
            pages.append((font, c))
    lines.append(r'\end{document}')
    return '\n'.join(lines) + '\n', pages


def top_centre(args):
    """The centre of the top of the ink on a page, in em from the left edge of the box of the character."""
    pdf, page = args
    with tempfile.TemporaryDirectory() as d:
        base = os.path.join(d, 'p')
        subprocess.run(['pdftoppm', '-r', str(DPI), '-gray', '-png', '-f', str(page), '-l', str(page), '-singlefile',
                        pdf, base], check=True)
        ink = np.asarray(Image.open(base + '.png')) < 128
    rows = np.where(ink.any(axis=1))[0]
    band = ink[rows[0]:rows[0] + int(round(BAND * SIZE / PT)) + 1]
    cols = np.where(band.any(axis=0))[0]
    return ((cols.min() + cols.max() + 1) / 2 * PT - LEFT) / SIZE


def measure(slots):
    tex, pages = document(slots)
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, 'm.tex'), 'w').write(tex)
        subprocess.run(['pdflatex', '-interaction=nonstopmode', 'm.tex'], cwd=d, check=True, capture_output=True)
        pdf = os.path.join(d, 'm.pdf')
        with Pool() as pool:
            tops = pool.map(top_centre, [(pdf, i + 1) for i in range(len(pages))], chunksize=4)
    return dict(zip(pages, tops))


if __name__ == '__main__':
    half, kern = metrics(REGULAR)
    half_bold, kern_bold = metrics(BOLD)
    slots = sorted(kern)
    assert all(c in kern_bold for c in slots)
    top = measure(slots)
    # Distance of the accent position from the centre of the top, in the stix2 fonts
    old = {c: half[c] + kern[c] - top[REGULAR, c] for c in slots}
    bold = {c: half_bold[c] + kern_bold[c] - top[BOLD, c] for c in slots}
    new = {c: round(top[REGULAR, c] + bold[c] - half[c], 3) for c in slots}
    latin = [c for c in slots if chr(c).isalpha()]
    print('# accent position right of the centre of the top, median over the %d Latin letters: %.3f em in %s,'
          % (len(latin), np.median([old[c] for c in latin]), REGULAR))
    print('# %.3f em in %s, and so in %s with the kerns below'
          % (np.median([bold[c] for c in latin]), BOLD, REGULAR))
    print('SANS_ITALIC = {%s}' % ', '.join("'%s': %.3f" % (NAMES.get(c, chr(c)), new[c]) for c in slots))
