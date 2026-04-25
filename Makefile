.PHONY: all doc test clean

all: doc test

doc:
	cd doc && latexmk -pdf -interaction=nonstopmode chetdoc.tex

test:
	cd test && latexmk -pdf -interaction=nonstopmode chetref_test.tex

clean:
	cd doc && latexmk -c chetdoc.tex && rm -f chetdocbib.bib *.bbl
	cd test && latexmk -c chetref_test.tex && rm -f *.bbl
