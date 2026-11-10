r"""Measure where subscripts should attach to the letters of the stix2 package, and print the shift tables of
newchet-subscripts.py.

TeX attaches a subscript at the width of a letter.  The script sets each letter alone, and each subscript alone at its
attachment point, with the metrics of the stix2 package (newchet's option nosubscriptkerns).  It renders every page and
records, for each pixel row, the right edge of the ink of the letter and the left edge of the ink of the subscript.  The
gap between a letter and a subscript is the smallest horizontal distance between the two inks over the rows where both
have ink.  A shift d moves the subscript left by d and reduces every gap by d.

The letters are the italic Latin and Greek letters and the partial sign of the math italic, the upright Latin letters,
Greek capitals and nabla of the upright font, and the calligraphic capitals.  There are 180 subscripts: the italic and
upright Latin letters, the lowercase Greek letters, the Greek capitals, the digits and the calligraphic capitals.  The
regular and bold weights are measured separately.  Bold math uses the regular calligraphic font, so only its regular
measurement counts.

The target is the median gap over the 26 italic lowercase letters, each with the subscripts a, n and i.  d brings the
mean gap of a letter with a, n and i to the target.  d is smaller where one of the 180 subscripts would then come closer
to the letter than it comes to any italic capital of the stix2 package.  Only positive d is used, so no subscript moves
away from its letter.  d below 0.005 em is left out.

Usage: python3 newchet-subscripts-measure.py.  It needs pdflatex, the newchet.sty of this folder, pdftoppm (poppler),
and the Python packages numpy and Pillow.  It renders 600 small pages at 4800 dpi, one at a time, deleting each image
after use.  It takes about a minute on eight cores.  Paste its output over the tables in newchet-subscripts.py.
"""
import os, re, subprocess, tempfile
from multiprocessing import Pool

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DPI = 4800
PT = 72.27 / DPI  # TeX points per pixel
SIZE = 10.0  # body size in pt, so one em of the text font
LEFT, TOP, DEPTH, WIDTH = 10.0, 16.0, 9.0, 50.0  # page geometry in pt: letter at LEFT, baseline TOP below the top

GREEK = ('alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi pi rho sigma tau upsilon phi chi psi '
         'omega varepsilon vartheta varpi varrho varsigma varphi').split()
CAPGREEK = 'Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega'.split()
UPPER = [chr(c) for c in range(65, 91)]
LOWER = [chr(c) for c in range(97, 123)]

# (font, name, TeX code, slot in the TFM)
LETTERS = ([('it', c, c, ord(c)) for c in UPPER + LOWER]
           + [('it', g, '\\' + g, 0x0B + i) for i, g in enumerate(GREEK)] + [('it', 'partial', '\\partial', 0x29)]
           + [('rm', c, '\\mathrm{%s}' % c, ord(c)) for c in UPPER + LOWER]
           + [('rm', g, '\\' + g, i) for i, g in enumerate(CAPGREEK)] + [('rm', 'nabla', '\\nabla', 0x28)]
           + [('cal', c, '\\mathcal{%s}' % c, ord(c)) for c in UPPER])
SUBSCRIPTS = ([('it', c, c) for c in UPPER + LOWER] + [('rm', c, '\\mathrm{%s}' % c) for c in UPPER + LOWER]
              + [('it', g, '\\' + g) for g in GREEK] + [('rm', g, '\\' + g) for g in CAPGREEK]
              + [('digit', str(i), str(i)) for i in range(10)] + [('cal', c, '\\mathcal{%s}' % c) for c in UPPER])


def document():
    """The TeX source and the list of pages.  A letter page sets the letter alone.  A subscript page sets the subscript
    on a white x, so that only the subscript has ink.  The log records the width at which each subscript attaches."""
    lines = [r'\documentclass{article}',
             r'\usepackage[stix2,nobib,nohyperref,notoc,notitlesec,notitlepage,nogeometry,nosubscriptkerns]{newchet}',
             r'\newcommand\pg[1]{\shipout\hbox{\vrule height %gpt depth %gpt width 0pt\kern%gpt #1}}' % (TOP, DEPTH, LEFT),
             r'\begin{document}\normalsize',
             r'\pdfpagewidth=%gpt \pdfpageheight=%gpt \pdfhorigin=0pt \pdfvorigin=0pt' % (WIDTH, TOP + DEPTH)]
    pages = []
    for bold in (0, 1):
        math = r'\boldmath' if bold else r'\unboldmath'
        for font, name, code, _ in LETTERS:
            lines.append(r'{%s\setbox0\hbox{$%s_{\kern-\scriptspace}$}\message{^^JATTACH \the\wd0^^J}\pg{$%s$}}'
                         % (math, code, code))
            pages.append(('letter', bold, font, name))
        for font, name, code in SUBSCRIPTS:
            lines.append(r'{%s\setbox0\hbox{$x_{\kern-\scriptspace}$}\message{^^JATTACH \the\wd0^^J}'
                         r'\pg{$\pdfliteral{1 g}x_{\pdfliteral{0 g}%s}$}}' % (math, code))
            pages.append(('sub', bold, font, name))
    lines.append(r'\end{document}')
    return '\n'.join(lines) + '\n', pages


def profile(args):
    """For each pixel row, the right edge of the ink of a letter or the left edge of that of a subscript, in pt from
    the attachment point.  Rows without ink give nan."""
    pdf, page, kind, attach = args
    with tempfile.TemporaryDirectory() as d:
        base = os.path.join(d, 'p')
        subprocess.run(['pdftoppm', '-r', str(DPI), '-gray', '-png', '-f', str(page), '-l', str(page), '-singlefile',
                        pdf, base], check=True)
        ink = np.asarray(Image.open(base + '.png')) < 128
    out = np.full(ink.shape[0], np.nan)
    for r in np.where(ink.any(axis=1))[0]:
        cols = np.where(ink[r])[0]
        out[r] = ((cols.max() if kind == 'letter' else cols.min()) + 0.5) * PT - LEFT - attach
    return out


def measure():
    tex, pages = document()
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, 'm.tex'), 'w').write(tex)
        env = dict(os.environ, TEXINPUTS=HERE + ':')
        subprocess.run(['pdflatex', '-interaction=nonstopmode', 'm.tex'], cwd=d, env=env, check=True,
                       capture_output=True)
        attach = [float(x) for x in re.findall(r'^ATTACH ([-\d.]+)pt', open(os.path.join(d, 'm.log')).read(), re.M)]
        assert len(attach) == len(pages)
        pdf = os.path.join(d, 'm.pdf')
        with Pool() as pool:
            prof = pool.map(profile, [(pdf, i + 1, p[0], attach[i]) for i, p in enumerate(pages)], chunksize=4)
    return dict(zip(pages, prof))


def gap(prof, letter, sub):
    """Smallest horizontal distance between the inks, in em."""
    a, b = prof[letter], prof[sub]
    rows = ~np.isnan(a) & ~np.isnan(b)
    return (b[rows] - a[rows]).min() / SIZE if rows.any() else np.inf


def shifts(prof, bold):
    subs = [('sub', bold, f, n) for f, n, _ in SUBSCRIPTS]
    ani = lambda f, n: np.mean([gap(prof, ('letter', bold, f, n), ('sub', bold, 'it', s)) for s in 'ani'])
    target = np.median([ani('it', c) for c in LOWER])
    capitals = [('letter', bold, 'it', c) for c in UPPER]
    floor = {s: min(gap(prof, c, s) for c in capitals) for s in subs}
    out = {}
    for font, name, _, slot in LETTERS:
        letter = ('letter', bold, font, name)
        d = min(ani(font, name) - target, min(gap(prof, letter, s) - floor[s] for s in subs))
        if d >= 0.005:
            out.setdefault(font, []).append((name, round(d, 3)))
    return target, out


if __name__ == '__main__':
    prof = measure()
    for bold in (0, 1):
        target, out = shifts(prof, bold)
        print('# %s: target gap %.3f em' % ('bold' if bold else 'regular', target))
        for font in ('it', 'rm', 'cal'):
            if bold and font == 'cal':
                continue
            var = {'it': 'ITALIC', 'rm': 'UPRIGHT', 'cal': 'CALLIGRAPHIC'}[font] + ('_BOLD' if bold else '')
            items = ', '.join("'%s': %.3f" % (n, d) for n, d in out.get(font, []))
            print('%s = {%s}' % (var, items))
