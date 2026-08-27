LATEXMK ?= latexmk
OUTDIR ?= build

.PHONY: all paper clean

all: paper

paper:
	mkdir -p $(OUTDIR)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
		-outdir=$(OUTDIR) main.tex

clean:
	$(LATEXMK) -C -outdir=$(OUTDIR) main.tex
