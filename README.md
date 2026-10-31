# chet

[![CTAN](https://img.shields.io/ctan/v/chet)](https://ctan.org/pkg/chet)
[![License: LPPL 1.3c](https://img.shields.io/badge/License-LPPL%201.3c-blue.svg)](https://www.latex-project.org/lppl/)

The `chet` package provides a streamlined LaTeX2e setup inspired by Paul
Ginsparg's `harvmac`. It gives papers the typographic look and feel of
`harvmac` while using standard LaTeX2e commands and environments.

**Author:** Andreas Stergiou (<andstergiou@gmail.com>)

See [doc/chetdoc.pdf](doc/chetdoc.pdf) for full documentation and examples.

## Contents

| File | Description |
| --- | --- |
| `chet.sty` | Main style file |
| `chetref.bst` | BibTeX bibliography style |
| `doc/chetdoc.tex` | Documentation and example |
| `doc/chetdoc.pdf` | Compiled documentation |
| `test/chetref_test.tex` | Test file for `chetref.bst` |
| `test/chetref_test.bib` | Test bibliography |
| `test/chetref_test.pdf` | Compiled test output |
| `newchet/newchet.sty` | New version of chet built on biblatex and titlesec (see [newchet](#newchet)) |
| `newchet/newchet-stix2-mathit.tfm`, `.vf` | Virtual font of the `stix2` option, which brings subscripts closer to italic letters (see [Subscripts with stix2](#subscripts-with-stix2)) |
| `newchet/newchet-stix2-mathit-bold.tfm`, `.vf` | The same for bold math |
| `newchet/newchet-stix2-mathcal.tfm`, `.vf` | The same for the calligraphic capitals of `\mathcal` |
| `newchet/newchet-subscripts.py` | Script that makes the six font files |
| `test/newchet_subscripts_test.tex` | Test file for the subscripts of the `stix2` option |

## Installation

**Via TeX Live / MiKTeX:** The package is on [CTAN](https://ctan.org/pkg/chet)
and is included in both distributions.

**Manually:** Copy `chet.sty` and `chetref.bst` into your project folder (or
anywhere on your TeX path).

## Usage

Add to your preamble:

```latex
\usepackage{chet}
```

Then compile with pdflatex and BibTeX:

```sh
pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper
```

### Options

| Option | Description |
| --- | --- |
| `mcite` | Enable grouped citations via [`mciteplus`](https://ctan.org/pkg/mciteplus): `\cite{a, *b, *c}` |
| `british` | Print "Acknowledgements" instead of "Acknowledgments" |
| `macrosonly` | Load only equation/section macros, without page layout (for conference proceedings) |

### Key commands

| Command | Description |
| --- | --- |
| `\eqn{...}[label]` | Display equation, numbered only if label given |
| `\eqna{...}[label]` | Aligned equation with single centred number |
| `\twoseqn`, `\threeseqn`, `\fourseqn` | Numbered subequation groups |
| `\newsec{title}[label]` | Section with optional label |
| `\subsec{title}[label]` | Subsection with optional label |
| `\subsubsec{title}[label]` | Subsubsection with optional label |
| `\rcite{key}` | Citation (shows key on margin in `\draftmode`) |
| `\draftmode` | Show equation/section labels in margins |
| `\toc` | Table of contents |
| `\foot{...}` | Footnote |
| `\ack{...}` | Acknowledgments section |
| `\email{addr}` | Email footnote (horizontal layout) |
| `\emailV{addr}` | Email footnote (vertical layout) |
| `\emails{addrs}` | Single email footnote with no mark |
| `\preprint{id}` | Preprint number (top right of title page) |

Labels defined with the optional argument are also available as `\labelname`
in subsequent text.

## newchet

`newchet/newchet.sty` is a new version of chet built on current packages. It keeps the chet title page and the chetref look of the bibliography. It uses biblatex instead of `chetref.bst`, titlesec for the section headings and tocloft for the table of contents. It is not yet on CTAN.

### Installation

Install newchet into your personal TeX tree, so that it works from any directory:

```sh
make install-newchet
```

This copies `newchet.sty` and the six font files of the `stix2` option into the tree that `kpsewhich -var-value TEXMFHOME` names: `~/Library/texmf` on macOS and `~/texmf` on Linux. `make install-newchet TEXMFHOME=/path/to/tree` installs into another tree. Give the tree as a full path. zsh, the default shell of macOS, does not expand the `~` in `TEXMFHOME=~/texmf`, so make then stops with a message. TeX searches the personal tree directly, so nothing else needs to be run. The tree holds copies, so run `make install-newchet` again after updating the repository. A tree with a file name database, such as `TEXMFLOCAL`, needs `mktexlsr` afterwards. With MiKTeX, copy the files into a root directory registered in the MiKTeX Console and refresh its file name database. By hand, the files go to these places in the tree:

| File | Folder in the tree |
| --- | --- |
| `newchet/newchet.sty` | `tex/latex/newchet/` |
| `newchet/newchet-stix2-mathit.tfm`, `newchet/newchet-stix2-mathit-bold.tfm`, `newchet/newchet-stix2-mathcal.tfm` | `fonts/tfm/newchet/` |
| `newchet/newchet-stix2-mathit.vf`, `newchet/newchet-stix2-mathit-bold.vf`, `newchet/newchet-stix2-mathcal.vf` | `fonts/vf/newchet/` |

A paper that has to compile on other computers, such as arXiv's or a co-author's, can carry newchet with it. Copy `newchet.sty` and the six font files into the paper's folder. newchet finds the fonts there too.

### Usage

```latex
\documentclass[11pt,a4paper]{article}
\usepackage{newchet}
\addbibresource{bibliography.bib}

\preprint{KCL-MTH-26-01}
\title{Title}
\author{A.~Author\email{a@example.com} \and B.~Author\email{b@example.com}}
\affiliation{Department, University}
\abstract{The abstract.}

\begin{document}
\maketitle
\toc
\section{Introduction}
...
\begin{acknowledgements}
We thank ...
\end{acknowledgements}
\printbibliography
\end{document}
```

Compile with pdflatex and biber:

```sh
pdflatex paper && biber paper && pdflatex paper && pdflatex paper
```

Bibliography entries read as J. Smith, B. Jones & D. Brown, *"Title"*, Journal **vol**, page (year), arXiv:XXXX.XXXXX [class]. The journal reference links to the DOI and the arXiv identifier links to arxiv.org. Entries are in citation order, and citations are sorted and compressed. A `collaboration` field prints "ATLAS Collaboration" before the authors. A JHEP article without a `doi` gets a DOI link inferred from its volume, year and page.

For grouped citations, load `\usepackage[mcite]{newchet}` and use biblatex's syntax, whose first key names the group: `\mcite{group1,*key1,*key2}`. chet's `\cite{key1, *key2}` would drop `key1`. Each member of a group starts on a new line.

`test/newchet_test.tex` checks the bibliography against the cases of `chetref_test.tex`. Build it with `make newchet-test`.

### Options

| Option | Description |
| --- | --- |
| `nobib` | Do not load biblatex (for revtex, `.bst` files or no bibliography) |
| `nogeometry` | Do not load geometry (the class or another package sets the margins) |
| `nohyperref` | Do not load hyperref. The bibliography then has no links, unless the document loads hyperref itself |
| `notoc` | Do not load tocloft or reformat the table of contents |
| `notitlesec` | Do not load titlesec or reformat the section headings |
| `notitlepage` | Keep the class's own `\maketitle` and abstract environment |
| `notheorems` | Do not define `theorem`, `proposition` and `conjecture` |
| `newtx` | Use newtxtext and newtxmath (Times) instead of Computer Modern; the title is then set in newtxtext too |
| `stix2` | Use STIX Two for text and math instead of Computer Modern; the title is then set in STIX Two too |
| `newtxgreek` | Take the math Greek letters from newtxmath, for example with `stix2`; `newtx` has them already |
| `nosubscriptkerns` | With `stix2`, keep the subscript placement of the stix2 package (see [Subscripts with stix2](#subscripts-with-stix2)) |
| `fontsize=11.5pt` | Set the body size to any value with `article`, `report` or `book`, which only offer 10pt, 11pt and 12pt |

The default font is Computer Modern. With Computer Modern, the text is spaced as in chet, so it looks less crammed: interword spaces are 1.2 times wider, lines are spread by 1.25 and the rows of multiline equations are 5pt apart instead of 3pt. chet widens the spaces of the body font alone, while newchet widens every Computer Modern roman font, so italics, bold, footnotes and the bibliography match the body. A `\linespread` or `\setlength{\jot}{...}` in the preamble overrides these values. If both `newtx` and `stix2` are given, the last one wins. Both work with pdflatex, so papers still compile on arXiv. STIX Two has no typewriter font, so with `stix2` the typewriter font is newtxtt. It is scaled to match the x-height of STIX Two and, unlike Computer Modern typewriter, it has a bold. STIX Two has no sans serif either, so `\textsf` and the caption labels stay in Computer Modern Sans. STIX Two Math puts the numerator and denominator of an inline fraction far from the bar, so newchet moves them closer and inline fractions no longer run into the lines around them. STIX Two has no bold for its large delimiters and its calligraphic, blackboard bold and typewriter math, so bold math, such as math in a section heading, uses their medium weight. The stix2 package does the same but warns for every font and size, while newchet does not. With `stix2`, scripts are 75% of the size and second-level scripts 60%, as stix2 sets them at 10pt. This holds at every size from 9pt up, so a 12pt body gets 9pt scripts instead of LaTeX's 8pt. With `stix2`, `\mathbb` is the blackboard bold of DSSerif, scaled by 1.025, which leaves its capitals 0.9% taller than the upright capitals of STIX Two. DSSerif has a bold weight, so `\mathbb` is bold in bold text, such as section headings. The AMS blackboard bold and that of STIX Two have none. newchet loads it with `\usepackage[bb=dsserif,bbscaled=1.025]{mathalpha}` at the end of the preamble. A document that loads mathalpha itself, after newchet, keeps its own options. For example, `\usepackage[bb=ams]{mathalpha}` gives the AMS blackboard bold and `\usepackage[bb=stixtwo]{mathalpha}` that of STIX Two. The option `newtxgreek` replaces the lowercase italic and uppercase upright Greek letters, and `\varkappa`, by those of newtxmath. The rest of the math keeps its font. The option `fontsize` scales the sizes and spacings of the 11pt class option, so `\normalsize` is exactly the size given and `\small`, `\large` and the others keep their 11pt proportions. It overrides the class's own size option. KOMA classes have their own `fontsize` option, so newchet ignores its option there. The title is 1.894 times the body size, the ratio of `\huge` to the body text at 11pt. It is 20.74pt at 11pt and 22.73pt at 12pt.

Any other option is passed to biblatex, for example `\usepackage[backend=bibtex]{newchet}`. Under the AMS, revtex, memoir and KOMA classes, newchet switches off tocloft, titlesec or the title page where they would clash with the class, and prints a warning.

### Subscripts with stix2

With `stix2`, newchet sets subscripts closer to italic and calligraphic letters than the stix2 package does. TeX attaches a subscript at the width of a letter and a superscript at its width plus its italic correction. The Type 1 metrics of STIX Two give most italic capitals a width that includes nearly all of their overhang. So a subscript starts beyond the top-right corner of V, W, Y, T, F, P and similar letters, far from their foot. newchet therefore uses two virtual fonts, `newchet-stix2-mathit` and `newchet-stix2-mathit-bold`. They draw the glyphs of the stix2 package unchanged. In them, 22 regular and 15 bold letters are narrower and have a larger italic correction, by the same amount. So only the subscripts move, by up to 0.18em, for T. Letters without scripts, superscripts, primes and accents keep their places. Limits are the one exception. TeX offsets the limits of an operator by half its italic correction. So when one of these letters carries limits, as in `\stackrel{*}{T}`, `\mathop{T}\limits^{a}_{b}` or `\mathop{V}^{a}_{b}` in display style, its upper limit moves right and its lower limit moves left, by half the subscript shift. That is up to 0.09em, for T. amsmath's `\overset` and `\underset` are not affected. The amounts come from the math italic of SticksToo. SticksToo is Michael Sharpe's reworking of STIX Two, with metrics tuned for TeX. newtxmath uses it with its `stickstoo` option. Regular a and g keep the metrics of the stix2 package. That package sets subscripts lower than SticksToo, so with SticksToo's amount they would almost touch the tail of a in script sizes. The g of SticksToo has a different outline, so its amount does not apply.

The calligraphic capitals of `\mathcal` have the same problem. Their width follows the top of the letter, and the flourish of N and the bars of F and T reach far to the right. So in $\mathcal{N}_{\mathcal{O}}$ the subscript sits far from the foot of N. A third virtual font, `newchet-stix2-mathcal`, moves the subscripts of F, I, J, N, P, T, V and W to the left, in the same way. N moves by 0.146em and T most, by 0.261em. SticksToo has no calligraphic font, so the amounts were measured from the outlines. The measure is the smallest horizontal distance between the ink of a letter and that of its subscript. Each amount brings the subscripts a, n and i to the median distance over the 26 capitals. It is smaller where one of 179 subscripts would then come closer to the letter than it comes to any capital of the stix2 package, as ξ would in $\mathcal{F}_\xi$ and b in $\mathcal{P}_b$. STIX Two has no bold calligraphic, so the font serves bold math too. The option `nosubscriptkerns` keeps the placement of the stix2 package for all three fonts.

A subscript j sits a little further from its letter than a subscript i, as in $\phi_j$ and $\phi_i$. Its tail hooks left below the baseline, and STIX Two keeps the tail inside the box of j. So the stem of j starts 0.15em further into its box than that of i. newchet cannot move j to the left in its font, since j would then run into a preceding parenthesis, bracket or bar. STIX Two sets `(` closer to the next letter than Computer Modern does. In `(j)` the gap is 0.04em, against 0.11em in Computer Modern. Where it matters, write `\phi_{\mkern-2mu j}`.

newchet uses the fonts only if it finds all six files. It asks `kpsewhich`, which the restricted shell escape of TeX Live allows by default, and it looks in the document folder. If it finds them in neither place, it warns and keeps the placement of the stix2 package. If kpsewhich cannot run, it looks only in the document folder. That happens with shell escape switched off, for example by `-no-shell-escape`. It also happens when an editor starts TeX without the TeX Live programs on its `PATH`. The fonts need no map file and no `updmap`, since they only point at the fonts of the stix2 package. They work with pdflatex, lualatex and xelatex, and with latex followed by dvips or dvipdfmx.

`make newchet-fonts` remakes the fonts with `newchet/newchet-subscripts.py`. It needs Python 3.7 or later and the TeX Live programs `kpsewhich`, `tftopl`, `vptovf` and `t1disasm`. It also needs the TeX Live packages stix2-type1 and stickstoo. This should rarely be needed, since the stix2 package plans no further updates to its Type 1 fonts. If a later stix2-type1 changes `stix2-mathit.tfm`, `stix2-mathit-bold.tfm` or `stix2-mathcal.tfm`, rerun `make newchet-fonts` and `make install-newchet`. Each virtual font records the version of the stix2 package it was made from, which `vftovp` shows. `test/newchet_subscripts_test.tex` sets every letter both ways, names the math italic in use and measures each shift. `make newchet-subscripts-test` builds it with the files of the repository. Compiled without make, it tests the installed newchet.

### Key commands

| Command | Description |
| --- | --- |
| `\preprint{id}` | Preprint number (top right of title page) |
| `\affiliation{...}` | Affiliations, in italics below the authors |
| `\abstract{...}` | Abstract on the title page (in the preamble) |
| `\date{...}` | Date at the bottom left of the title page (default: current month and year) |
| `\email{addr}` | Email footnote (horizontal layout) |
| `\emailV{addr}` | Email footnote (vertical layout) |
| `\emails{addrs}` | Single email footnote with no mark |
| `$\titlemath{...}$` | Math in the title, in the title font |
| `\toc` | Table of contents |
| `acknowledgements` | Acknowledgements section (also `acknowledgments`) |
| `\ack{...}` | Shortcut for the `acknowledgements` environment |

Theorem notes, such as "(Main result)", are set in bold to match the theorem head. This applies to the `plain` and `definition` theorem styles.

## License

[LPPL 1.3c](LICENSE) — see also [CHANGELOG.md](CHANGELOG.md).
