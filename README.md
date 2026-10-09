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

Copy `newchet.sty` into your personal TeX tree, so that it works from any directory:

```sh
mkdir -p ~/Library/texmf/tex/latex/newchet
cp newchet/newchet.sty ~/Library/texmf/tex/latex/newchet/
```

On Linux the personal tree is `~/texmf` instead of `~/Library/texmf`. You can also copy `newchet.sty` into your project folder.

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
| `nohyperref` | Do not load hyperref |
| `notoc` | Do not load tocloft or reformat the table of contents |
| `notitlesec` | Do not load titlesec or reformat the section headings |
| `notitlepage` | Keep the class's own `\maketitle` and abstract environment |
| `notheorems` | Do not define `theorem`, `proposition` and `conjecture` |

Any other option is passed to biblatex, for example `\usepackage[backend=bibtex]{newchet}`. Under the AMS, revtex, memoir and KOMA classes, newchet switches off tocloft, titlesec or the title page where they would clash with the class, and prints a warning.

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
