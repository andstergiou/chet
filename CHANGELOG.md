# Changelog

All notable changes to the chet package are recorded here.

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
