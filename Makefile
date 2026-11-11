.PHONY: all doc test newchet-test newchet-subscripts-test newchet-accents-test newchet-fonts install-newchet clean

# The personal TeX tree: ~/Library/texmf on macOS, ~/texmf on Linux.  Override it with a
# full path, e.g. make install-newchet TEXMFHOME=/path/to/tree.  zsh passes a ~ there unexpanded.
TEXMFHOME := $(shell kpsewhich -var-value TEXMFHOME)
NEWCHET_FONTS := newchet-stix2-mathit newchet-stix2-mathit-bold newchet-stix2-mathrm newchet-stix2-mathrm-bold newchet-stix2-mathcal newchet-stix2-mathsfit

all: doc test

doc:
	cd doc && latexmk -pdf -interaction=nonstopmode chetdoc.tex

test: newchet-test newchet-subscripts-test newchet-accents-test
	cd test && latexmk -pdf -interaction=nonstopmode chetref_test.tex

# newchet.sty is found through TEXINPUTS; latexmk runs biber
newchet-test:
	cd test && TEXINPUTS=../newchet: latexmk -pdf -interaction=nonstopmode newchet_test.tex

# The virtual fonts of the stix2 option are found through TFMFONTS and VFFONTS
newchet-subscripts-test:
	cd test && TEXINPUTS=../newchet: TFMFONTS=../newchet: VFFONTS=../newchet: latexmk -pdf -interaction=nonstopmode newchet_subscripts_test.tex

newchet-accents-test:
	cd test && TEXINPUTS=../newchet: TFMFONTS=../newchet: VFFONTS=../newchet: latexmk -pdf -interaction=nonstopmode newchet_accents_test.tex

# Remake the virtual fonts of the stix2 option from the metrics of stix2, the shifts in newchet-subscripts.py and the
# kerns in newchet-accents.py.  python3 newchet/newchet-subscripts-measure.py measures the shifts again, and
# python3 newchet/newchet-accents-measure.py the kerns.
newchet-fonts:
	cd newchet && python3 newchet-subscripts.py && python3 newchet-accents.py

# Copy newchet.sty and the virtual fonts of the stix2 option into the personal tree
install-newchet:
	@case "$(TEXMFHOME)" in /*|?:*) ;; *) echo "TEXMFHOME is '$(TEXMFHOME)'. Give the tree as a full path, such as TEXMFHOME=$$HOME/texmf." >&2; exit 1;; esac
	mkdir -p "$(TEXMFHOME)/tex/latex/newchet" "$(TEXMFHOME)/fonts/tfm/newchet" "$(TEXMFHOME)/fonts/vf/newchet"
	cp newchet/newchet.sty "$(TEXMFHOME)/tex/latex/newchet/"
	cp $(NEWCHET_FONTS:%=newchet/%.tfm) "$(TEXMFHOME)/fonts/tfm/newchet/"
	cp $(NEWCHET_FONTS:%=newchet/%.vf) "$(TEXMFHOME)/fonts/vf/newchet/"

clean:
	cd doc && latexmk -c chetdoc.tex && rm -f chetdocbib.bib *.bbl
	cd test && latexmk -c chetref_test.tex && rm -f *.bbl
	cd test && latexmk -c newchet_test.tex && rm -f *.bbl
	cd test && latexmk -c newchet_subscripts_test.tex
	cd test && latexmk -c newchet_accents_test.tex
