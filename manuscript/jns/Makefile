TECTONIC ?= tectonic
PYTHON ?= python3

.PHONY: all paper figures test clean

all: paper

figures:
	$(PYTHON) figures/generate_figures.py

paper: figures
	$(TECTONIC) main.tex --keep-intermediates --keep-logs --outdir build

test:
	cd ../.. && $(PYTHON) -m pytest -q

clean:
	find build -type f -delete
