% chetref.bst
% Copyright 2026 Andreas Stergiou
%
% This work may be distributed and/or modified under the
% conditions of the LaTeX Project Public License, either version 1.3
% of this license or (at your option) any later version.
% The latest version of this license is in
%   http://www.latex-project.org/lppl.txt
% and version 1.3 or later is part of all distributions of LaTeX
% version 2005/12/01 or later.

ENTRY
  { address
    author
    archive
    booktitle
    chapter
    collaboration
    doi
    edition
    editor
    eprint
    howpublished
    institution
    journal
    key
    month
    note
    number
    organization
    pages
    publisher
    school
    series
    SLACcitation
    title
    type
    primaryClass
    url
    volume
    year
  }
  {}
  { label }

STRINGS { s t }

FUNCTION {not}
{   { #0 }
    { #1 }
  if$
}

FUNCTION {and}
{   'skip$
    { pop$ #0 }
  if$
}

FUNCTION {or}
{   { pop$ #1 }
    'skip$
  if$
}

INTEGERS { nameptr namesleft numnames }

FUNCTION {format.names}
{ 's :=
  #1 'nameptr :=
  s num.names$ 'numnames :=
  numnames 'namesleft :=
    { namesleft #0 > }
    { s nameptr "{f.~}{vv~~}{ll}{,~jj}" format.name$ 't :=
      nameptr #1 >
    { namesleft #1 >
        { ", " * t * }
        { t "others" =
        { " et~al." * }
        { " \& " * t * }
          if$
        }
      if$
    }
    't
      if$
      nameptr #1 + 'nameptr :=
      namesleft #1 - 'namesleft :=
    }
  while$
}

FUNCTION {first.page}
{ 't :=
  ""
  { t empty$ not
    t #1 #1 substring$ duplicate$ "-" = not
                 swap$ duplicate$ "," = not
                            swap$ "+" = not
    and and and }
    {
      t #1 #1 substring$ *
      t #2 global.max$ substring$ 't :=
    }
  while$
}

INTEGERS { output.state }

FUNCTION {output}
{
  's :=
  s empty$
    'skip$
    {
      output.state #1 =
        { ", " write$ newline$  }
        { #1 'output.state := }
      if$
      s write$
    }
  if$
}

FUNCTION {begin.entry}
{
  "\bibitem{" cite$ * "}" * write$ newline$
  #0 'output.state :=
}

FUNCTION {fin.entry}
{
  "\mciteBstWouldAddEndPuncttrue" write$ newline$
  "\mciteSetBstMidEndSepPunct{\mcitedefaultmidpunct\newline}" write$ newline$
  "{\mcitedefaultendpunct}{\mcitedefaultseppunct}\relax" write$ newline$
  "\EndOfBibitem" write$
}

FUNCTION {format.authors}
{
  collaboration empty$
    { "" }
    { author empty$
        { collaboration " Collaboration" * }
        { collaboration " Collaboration, " * }
      if$
    }
  if$
  author empty$
    { "" }
    { author format.names }
  if$
  *
}

FUNCTION {format.url}
{
  url empty$
    { "" }
    { "\href{" url * "}{\nolinkurl{" * url * "}}" * }
  if$
}

FUNCTION {format.editor}
{
  editor empty$
    { "" }
    { "ed: " editor format.names * }
  if$
}

FUNCTION {format.title}
{ title empty$
    { "" }
    { "\textit{``" title * "''}" *}
  if$
}

STRINGS { nvol ndoi }

FUNCTION {format.journal}
{
  journal empty$
    { "" }
    {
      volume empty$ { "no volume for journal in " cite$ * warning$ } 'skip$ if$
      pages empty$ { "no pages for journal in " cite$ * warning$ } 'skip$ if$
      year empty$ { "no year for journal in " cite$ * warning$ } 'skip$ if$

      volume 'nvol :=

      journal "JHEP" = nvol text.length$ #2 = and
        { year #3 #2 substring$ nvol * 'nvol := }
        'skip$
      if$

      doi empty$ { "" } { doi } if$ 'ndoi :=

      journal "JHEP" = ndoi "" = and
        {
          year #1 #3 substring$ "200" = year #1 #3 substring$ "199" = or
          {
            "10.1088/1126-6708/" year *
            "/" * nvol #3 #2 substring$ *
            "/" * pages first.page *
            'ndoi :=
          }
          {
            "10.1007/JHEP" nvol #3 #2 substring$ * "(" * year * ")" * pages first.page *
            'ndoi :=
          }
        if$
        }
        'skip$
      if$
      ""
      ndoi "" = { } { "\doiref{" * ndoi * "}{" * } if$
      journal *
      " \textbf{" *
      nvol *
      "}, " *
      pages first.page *
      year empty$
        { }
        { " (" * year * ")\ignorespaces" * }
      if$
      ndoi "" = { } { "}" * } if$
      "\ignorespaces" *
    }
  if$
}

INTEGERS { spacen spacepos }

FUNCTION { formatarxiv }
{
  's :=
  s #1 #6 substring$ "arXiv:" =
  {
    s #7 s text.length$ #6 - substring$ 's :=
  }
  'skip$
  if$

  s text.length$ 'spacen :=
  #0 'spacepos :=
  { spacepos spacen < }
  { spacepos #1 + 'spacepos :=
    s spacepos #1 substring$ " " =
      {
        spacepos #1 - 'spacen :=
        s #1 spacen substring$ 's :=
      }
      'skip$
    if$
  }
  while$
  s
}

FUNCTION { arxivprefix }
{
  's :=
  s #1 #1 substring$ chr.to.int$ "0" chr.to.int$ <
  s #1 #1 substring$ chr.to.int$ "9" chr.to.int$ > +
  'skip$
  {
    "arXiv:" s * 's :=
  }
  if$
  s
}

FUNCTION {format.primaryClass}
{
  primaryClass empty$
      { "" }
      { " \![" primaryClass * "]" *}
  if$
}

FUNCTION { format.eprint }
{ eprint empty$
    { "" }
    { "\texttt{\arxivref{" eprint formatarxiv * "}{" * eprint formatarxiv arxivprefix * format.primaryClass * "}}\ignorespaces" * }
  if$
}

FUNCTION {format.note}
{ note empty$
    { "" }
    { note "\ignorespaces" * }
  if$
}

FUNCTION {format.date}
{ year empty$
    { "" }
    { " (" year * ")\ignorespaces" *}
  if$
}

FUNCTION {format.publisher}
{ publisher empty$
    { "" }
    { publisher format.date *}
  if$
}

FUNCTION {format.address}
{ address empty$
    { "" }
    { address }
  if$
}

FUNCTION {format.edition}
{ edition empty$
    { "" }
    { edition "l" change.case$ " edition" * }
  if$
}

FUNCTION {format.pages}
{ pages empty$
    { "" }
    { "p.~" pages * "\ignorespaces" *}
  if$
}

FUNCTION {article}
{
  crossref missing$ 'skip$ { "crossref in " cite$ * warning$} if$
  author missing$ collaboration missing$ and { "author missing in " cite$ * warning$} 'skip$ if$
  title missing$ journal missing$ and eprint missing$ and note missing$ and { "title, journal, eprint and note missing in " cite$ * warning$} 'skip$ if$
  begin.entry
  format.authors output
  format.title output
  format.journal output
  format.eprint output
  format.note output
  format.url output
  fin.entry
}


FUNCTION {book}
{
  crossref missing$ 'skip$ { "crossref in " cite$ * warning$} if$
  author missing$ editor missing$ and { "author and editor missing in " cite$ * warning$} 'skip$ if$
  title missing$ { "title missing in " cite$ * warning$} 'skip$ if$
  publisher missing$ { "publisher missing in " cite$ * warning$} 'skip$ if$

  begin.entry
  format.authors output
  format.editor output
  format.title output
  format.edition output
  format.publisher output
  format.address output
  format.pages output
  format.eprint output
  format.note output
  format.url output
  fin.entry
}

FUNCTION {inbook}
{
  author missing$ editor missing$ and { "author and editor missing in " cite$ * warning$} 'skip$ if$
  title missing$ { "title missing in " cite$ * warning$} 'skip$ if$
  booktitle missing$ { "booktitle missing in " cite$ * warning$} 'skip$ if$
  begin.entry
  format.authors output
  format.title output
  booktitle empty$ 'skip$ { "in \textit{``" booktitle * "''}" * output } if$
  format.edition output
  format.editor output
  format.pages output
  format.publisher output
  format.address output
  format.eprint output
  format.note output
  format.url output
  fin.entry
}

FUNCTION {inproceedings} { inbook }

FUNCTION {conference} { inbook }

FUNCTION {incollection} { inbook }

FUNCTION {misc}
{
  begin.entry
  format.authors output
  format.title output
  howpublished empty$ 'skip$ { howpublished output } if$
  format.eprint output
  format.note output
  format.url output
  fin.entry
}

FUNCTION {unpublished} { misc }

FUNCTION {phdthesis}
{
  author missing$ { "author missing in " cite$ * warning$} 'skip$ if$
  title missing$ { "title missing in " cite$ * warning$} 'skip$ if$
  school missing$ { "school missing in " cite$ * warning$} 'skip$ if$
  begin.entry
  format.authors output
  format.title output
  school empty$
    { "PhD thesis" format.date * }
    { "PhD thesis, " school * format.date * }
  if$ output
  format.eprint output
  format.note output
  format.url output
  fin.entry
}

FUNCTION {mastersthesis}
{
  author missing$ { "author missing in " cite$ * warning$} 'skip$ if$
  title missing$ { "title missing in " cite$ * warning$} 'skip$ if$
  school missing$ { "school missing in " cite$ * warning$} 'skip$ if$
  begin.entry
  format.authors output
  format.title output
  school empty$
    { "Master's thesis" format.date * }
    { "Master's thesis, " school * format.date * }
  if$ output
  format.eprint output
  format.note output
  format.url output
  fin.entry
}

FUNCTION {techreport}
{
  author missing$ { "author missing in " cite$ * warning$} 'skip$ if$
  title missing$ { "title missing in " cite$ * warning$} 'skip$ if$
  begin.entry
  format.authors output
  format.title output
  institution empty$ 'skip$ { institution output } if$
  number empty$
    { year empty$ { "" } { "(" year * ")\ignorespaces" * } if$ }
    { "Report No. " number * format.date * }
  if$ output
  format.eprint output
  format.note output
  format.url output
  fin.entry
}

FUNCTION {default.type} { article }

READ

STRINGS { longest.label }

INTEGERS { number.label longest.label.width }

FUNCTION {initialize.longest.label}
{ "" 'longest.label :=
  #1 'number.label :=
  #0 'longest.label.width :=
}

FUNCTION {longest.label.pass}
{ number.label int.to.str$ 'label :=
  number.label #1 + 'number.label :=
  label width$ longest.label.width >
    { label 'longest.label :=
      label width$ 'longest.label.width :=
    }
    'skip$
  if$
}

EXECUTE {initialize.longest.label}

ITERATE {longest.label.pass}

FUNCTION {begin.bib}
{ preamble$ empty$
    'skip$
    { preamble$ write$ newline$ }
  if$
  "%bibliography generated by chetref.bst" write$ newline$
  "\ifx\mcitethebibliography\mciteundefinedmacro" write$ newline$
  "  \let\mcitethebibliography\thebibliography" write$ newline$
  "  \expandafter\let\csname endmcitethebibliography\endcsname\endthebibliography" write$ newline$
  "  \def\mcitedefaultmidpunct{,~}" write$ newline$
  "  \def\mcitedefaultendpunct{.}" write$ newline$
  "  \def\mcitedefaultseppunct{;}" write$ newline$
  "  \def\EndOfBibitem{}" write$ newline$
  "  \def\mciteBstWouldAddEndPuncttrue{}" write$ newline$
  "  \def\mciteBstWouldAddEndPunctfalse{}" write$ newline$
  "  \def\mciteSetBstMidEndSepPunct#1#2#3{#2}" write$ newline$
  "\fi" write$ newline$
  "\begin{mcitethebibliography}{"  longest.label  * "}" * write$ newline$
  "\ifx\href\asklfhas\newcommand{\href}[2]{#2}\fi" write$ newline$
  "\ifx\arxivref\asklfhas\newcommand{\arxivref}[2]{\href{https://arxiv.org/abs/#1}{#2}}\fi" write$ newline$
  "\ifx\doiref\asklfhas\newcommand{\doiref}[2]{\href{https://doi.org/#1}{#2}}\fi" write$ newline$
  "\parskip 0pt" write$ newline$
  "\normalsize" write$ newline$
  newline$
}

EXECUTE {begin.bib}

ITERATE {call.type$}

FUNCTION {end.bib}
{
  "\end{mcitethebibliography}" write$ newline$
}

EXECUTE {end.bib}
