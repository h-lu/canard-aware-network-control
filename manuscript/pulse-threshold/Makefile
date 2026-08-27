LATEXMK ?= latexmk

.PHONY: all paper clean

all: paper

paper:
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	$(LATEXMK) -C main.tex

