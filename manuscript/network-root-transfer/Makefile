LATEXMK ?= latexmk
PYTHON ?= python3
UV ?= uv
PAPER_FIGURES := \
	figures/delay-moment-map.pdf \
	figures/connection-geometry.pdf
PAPER_A_TESTS := \
	tests/test_paper_a_jns_rewrite_contract.py \
	tests/test_block_schur_response.py \
	tests/test_canard_conditioning.py \
	tests/test_heterogeneous_curvature_root.py \
	tests/test_leading_delay_moment.py \
	tests/test_lifted_selected_root_response.py \
	tests/test_multiple_recovery_center.py \
	tests/test_nonlocal_graph_jet.py \
	tests/test_outer_selection_coherence.py \
	tests/test_reduced_canard_root.py \
	tests/test_shared_recovery_moment.py \
	tests/test_shared_resource_markov.py \
	tests/test_shared_resource_response.py \
	tests/test_strong_unstable_history.py \
	tests/test_transverse_lin_sweep.py \
	tests/test_transverse_modes.py

.PHONY: all paper figure check clean

all: paper

figure: $(PAPER_FIGURES)

figures/delay-moment-map.pdf: figures/delay_moment_map.py
	$(PYTHON) figures/delay_moment_map.py --output $@

figures/connection-geometry.pdf: figures/connection_geometry.py
	$(PYTHON) figures/connection_geometry.py --output $@

paper: $(PAPER_FIGURES)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error supplement.tex
	$(LATEXMK) -g -pdf -interaction=nonstopmode -halt-on-error main.tex
	$(LATEXMK) -g -pdf -interaction=nonstopmode -halt-on-error supplement.tex

check:
	cd ../.. && $(UV) run --extra test pytest -q $(PAPER_A_TESTS)

clean:
	@if command -v $(LATEXMK) >/dev/null 2>&1; then \
		$(LATEXMK) -C main.tex; \
		$(LATEXMK) -C supplement.tex; \
	fi
	$(RM) main.bbl supplement.bbl
	@if [ -d build ]; then find build -type f -delete; fi
