# Changelog

All notable changes to the chet package are recorded here.

## [newchet 1.0] — 2026-10-09

- Added `newchet/newchet.sty`, a new version of chet built on current packages: biblatex replaces `chetref.bst` with a chetref-like style, titlesec sets the headings, and hyperref, geometry, tocloft and microtype are configured
- The bibliography reproduces every case of `test/chetref_test.tex`: collaborations, et al. without a comma, `arXiv:` prefixes, editions, Master's theses, grouped citations via `\mcite` and JHEP DOI inference; JHEP DOIs are inferred for all years (IOP up to 2008, Springer from 2009), not only those starting 199 or 201
- `test/newchet_test.tex` and `make newchet-test` check the bibliography against the chetref cases
- Title page as in `chet.sty`, with `\preprint`, `\affiliation`, `\abstract`, `\email`, `\emailV`, `\emails` and `\titlemath`; the title font is the T1 version of chet's scaled `cmr10`
- `acknowledgements` environment and `\ack`, with British spelling by default
- The References heading is centred and set at the body size like the Acknowledgements heading, as in `chet.sty`, with or without titlesec, and the space below it is cut to match `chet.sty`
- Appendices are headed "Appendix A." in the heading and the table of contents, as in `chet.sty`
- Theorem notes are bold in the `plain` and `definition` styles, matching the head
- The title is 1.894 times the body size, the ratio `\huge` has at 11pt, instead of `\huge`, which jumps to 24.88pt at 12pt; with Computer Modern, fix-cm supplies the in-between sizes, also for math in the title
- Options `newtx` and `stix2` set text and math in newtx (Times) or STIX Two instead of Computer Modern; the title and `\titlemath` use the same text font, and the last of the two options given wins
- With `stix2`, typewriter text is set in newtxtt, which has a bold, scaled by 1.02 to match the x-height of STIX Two Text; fix-cm is now loaded with every font option, so the Computer Modern Sans caption labels follow any body size
- Option `newtxgreek` takes the math Greek letters from newtxmath, for example on top of STIX Two
- Option `fontsize=<size>` sets any body size with `article`, `report` or `book`, by scaling the sizes and spacings of the 11pt class option
- Options `nobib`, `nogeometry`, `nohyperref`, `notoc`, `notitlesec`, `notitlepage` and `notheorems`; incompatible parts are switched off automatically for the AMS, revtex, memoir and KOMA classes

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
