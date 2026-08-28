LATEXMK ?= latexmk
PYTHON ?= python3
ROOT_FIGURE := figures/root-mechanism.pdf

.PHONY: all paper figure clean

all: paper

figure: $(ROOT_FIGURE)

$(ROOT_FIGURE): figures/root_mechanism.py
	$(PYTHON) figures/root_mechanism.py --output $(ROOT_FIGURE)

paper: $(ROOT_FIGURE)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error supplement.tex
	$(LATEXMK) -g -pdf -interaction=nonstopmode -halt-on-error main.tex
	$(LATEXMK) -g -pdf -interaction=nonstopmode -halt-on-error supplement.tex

clean:
	@if command -v $(LATEXMK) >/dev/null 2>&1; then \
		$(LATEXMK) -C main.tex; \
		$(LATEXMK) -C supplement.tex; \
	fi
	$(RM) main.bbl supplement.bbl
	find build -type f -delete
