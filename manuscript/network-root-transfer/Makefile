TECTONIC ?= tectonic
LATEXMK ?= latexmk
PYTHON ?= python3
ROOT_FIGURE := figures/root-mechanism.pdf

.PHONY: all paper figure clean

all: paper

figure: $(ROOT_FIGURE)

$(ROOT_FIGURE): figures/root_mechanism.py
	$(PYTHON) figures/root_mechanism.py --output $(ROOT_FIGURE)

paper: $(ROOT_FIGURE)
	@if command -v $(TECTONIC) >/dev/null 2>&1; then \
		$(TECTONIC) main.tex --keep-intermediates --keep-logs --outdir build; \
	else \
		$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex; \
	fi

clean:
	@if command -v $(LATEXMK) >/dev/null 2>&1; then $(LATEXMK) -C main.tex; fi
	find build -type f -delete
