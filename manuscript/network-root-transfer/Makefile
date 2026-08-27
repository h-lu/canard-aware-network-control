TECTONIC ?= tectonic
LATEXMK ?= latexmk

.PHONY: all paper clean

all: paper

paper:
	@if command -v $(TECTONIC) >/dev/null 2>&1; then \
		$(TECTONIC) main.tex --keep-intermediates --keep-logs --outdir build; \
	else \
		$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex; \
	fi

clean:
	@if command -v $(LATEXMK) >/dev/null 2>&1; then $(LATEXMK) -C main.tex; fi
	find build -type f -delete
