# Changelog

All notable changes to the chet package are recorded here.

## [newchet 1.0] — 2026-10-31

- Added `newchet/newchet.sty`, a new version of chet built on current packages: biblatex replaces `chetref.bst` with a chetref-like style, titlesec sets the headings, and hyperref, geometry, tocloft and microtype are configured
- The bibliography reproduces every case of `test/chetref_test.tex`: collaborations, et al. without a comma, `arXiv:` prefixes, editions, Master's theses, grouped citations via `\mcite` and JHEP DOI inference; JHEP DOIs are inferred for all years (IOP up to 2008, Springer from 2009), not only those starting 199 or 201
- `test/newchet_test.tex` and `make newchet-test` check the bibliography against the chetref cases
- Title page as in `chet.sty`, with `\preprint`, `\affiliation`, `\abstract`, `\email`, `\emailV`, `\emails` and `\titlemath`; the title font is the T1 version of chet's scaled `cmr10`
- `acknowledgements` environment and `\ack`, with British spelling by default
- The References heading is centred and set at the body size like the Acknowledgements heading, as in `chet.sty`, with or without titlesec, and the space below it is cut to match `chet.sty`. It is listed in the table of contents without a number, also as in `chet.sty`
- Appendices are headed "Appendix A." in the heading and the table of contents, as in `chet.sty`
- In the table of contents, a number too long for its box, such as 10. or 3.10., gets a wider box. This also works with tocloft before v3.0, which lacks the hook newchet uses for it, as on Overleaf
- Theorem notes are bold in the `plain` and `definition` styles, matching the head
- The title is 1.894 times the body size, the ratio `\huge` has at 11pt, instead of `\huge`, which jumps to 24.88pt at 12pt; with Computer Modern, fix-cm supplies the in-between sizes, also for math in the title
- Options `newtx` and `stix2` set text and math in newtx (Times) or STIX Two instead of Computer Modern; the title and `\titlemath` use the same text font, and the last of the two options given wins
- With Computer Modern, the text is spaced as in `chet.sty`: interword spaces 1.2 times wider, `\linespread{1.25}` and a `\jot` of 5pt; every Computer Modern roman font is widened, not only the body font, so italics, bold, footnotes and the bibliography match the body
- With `stix2`, typewriter text is set in newtxtt, which has a bold, scaled by 1.02 to match the x-height of STIX Two Text; fix-cm is now loaded with every font option, so the Computer Modern Sans caption labels follow any body size
- With `stix2`, the numerator and denominator of an inline fraction sit 0.08em from the bar instead of about 0.3em, so inline fractions no longer run into the lines around them; scripts are 75% and second-level scripts 60% of the size from 9pt up, the ratios stix2 uses at 10pt, instead of LaTeX's fixed 8pt and 6pt at 11pt and 12pt
- With `stix2`, bold math takes the medium weight of the large delimiters and of the calligraphic, blackboard bold and typewriter math directly, since STIX Two has no bold for them. The stix2 package substitutes it too, but warns for every font and size, so each bold heading with math gave 15 font warnings
- With `stix2`, `\mathbb` is the blackboard bold of DSSerif scaled by 1.025, which has a bold weight, through `\usepackage[bb=dsserif,bbscaled=1.025]{mathalpha}` at the end of the preamble, unless the document loads mathalpha itself
- Script sizes that LaTeX calculates, for sizes it does not declare, such as `\tiny` with `fontsize=`, are at least 5pt, as its declared ones are, but never larger than the text
- Option `newtxgreek` takes the math Greek letters from newtxmath, for example on top of STIX Two
- With `stix2`, subscripts sit closer to italic letters, as in SticksToo. The virtual fonts `newchet-stix2-mathit` and `newchet-stix2-mathit-bold` draw the glyphs of the stix2 package and move only the subscripts. The subscript of T moves most, by 0.18em. Superscripts, primes and accents keep their places. Limits on these letters, such as the label of `\stackrel{*}{T}`, move by half as much
- With `stix2`, subscripts also sit closer to the calligraphic capitals of `\mathcal`, such as N in $\mathcal{N}_{\mathcal{O}}$. The virtual font `newchet-stix2-mathcal` moves the subscripts of F, I, J, N, P, T, V and W, by amounts measured from the outlines, since SticksToo has no calligraphic font. N moves by 0.146em and T most, by 0.261em. The font also serves bold math, since STIX Two has no bold calligraphic
- newchet uses these fonts when kpsewhich finds all six files, or when all six are in the document folder. Otherwise it keeps the subscript placement of the stix2 package and warns. The option `nosubscriptkerns` keeps that placement without a warning
- `newchet/newchet-subscripts.py` makes the fonts, and `make newchet-fonts` runs it. `make install-newchet` copies the fonts and `newchet.sty` into the personal TeX tree. `test/newchet_subscripts_test.tex` sets every letter both ways, and `make newchet-subscripts-test` builds it
- Of `newtx` and `stix2`, the last one given now wins, as documented. `\ProcessOptions*` takes the options in the order given. Before, `stix2` always won
- Option `fontsize=<size>` sets any body size with `article`, `report` or `book`, by scaling the sizes and spacings of the 11pt class option
- Options `nobib`, `nogeometry`, `nohyperref`, `notoc`, `notitlesec`, `notitlepage` and `notheorems`; incompatible parts are switched off automatically for the AMS, revtex, memoir and KOMA classes. With `nohyperref`, the DOI and arXiv references are printed without links, unless the document loads hyperref itself

## [2.3b] — 2026-07-11

- Fix hyperref duplicate anchors in appendices: Define `\theHsection` when redefining `\appendix`, resolving duplicate anchor IDs (e.g. equation.1.1 vs equation.A.1) that cause links to jump to the main body instead of the appendix.

## [2.3a] — 2026-04-26

- Version number synchronised with CTAN release

## [2.3] — 2026

- Added `mcite` package option, enabling grouped citations via `mciteplus`
- Added `british` package option for "Acknowledgements" spelling
- Added `macrosonly` option for use with external style files
- `chetref.bst`: added `misc`, `unpublished`, `phdthesis`, `mastersthesis`,
  `techreport`, `inproceedings`, `conference`, and `incollection` entry types
- `chetref.bst`: fixed `inbook` and `inproceedings` missing `fin.entry` call
- `chetref.bst`: fixed collaboration-only entries producing a double comma
- `chetref.bst`: fixed `book` ignoring the `editor` field for edited volumes
- `chetref.bst`: fixed `article` warning spuriously when only `collaboration` is set
- `chetref.bst`: URLs now use `\nolinkurl` for correct line-breaking
- `chetref.bst`: removed dead code (`n.dashify`, `multi.page.check`,
  `field.or.null`, `format.btitle`, `output.spires`, `puttilde`)

## [1.0] — 2011

- Initial release
