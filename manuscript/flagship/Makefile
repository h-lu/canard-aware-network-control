TECTONIC ?= tectonic

.PHONY: all paper clean

all: paper

paper:
	$(TECTONIC) main.tex --keep-intermediates --keep-logs --outdir build

clean:
	find build -type f -delete
