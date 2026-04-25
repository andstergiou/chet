# chet

[![CTAN](https://img.shields.io/ctan/v/chet)](https://ctan.org/pkg/chet)
[![License: LPPL 1.3c](https://img.shields.io/badge/License-LPPL%201.3c-blue.svg)](https://www.latex-project.org/lppl/)

The `chet` package provides a streamlined LaTeX2e setup inspired by Paul
Ginsparg's `harvmac`. It gives papers the typographic look and feel of
`harvmac` while using standard LaTeX2e commands and environments.

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

## License

[LPPL 1.3c](LICENSE) — see also [CHANGELOG.md](CHANGELOG.md).
