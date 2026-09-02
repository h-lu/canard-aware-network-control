LATEXMK ?= latexmk
UV ?= uv
PAPER_PYTHON ?= $(UV) run --extra paper python
THREE_NODE_DATA := ../../experiments/results/three_node_finite_section_diagnostic.json
GROWING_NETWORK_DATA := ../../experiments/results/growing_network_finite_section_diagnostic.json
PAPER_FIGURES := \
	figures/connection-geometry.pdf \
	figures/three-node-finite-section.pdf
PAPER_A_TESTS := \
	tests/test_paper_a_jns_rewrite_contract.py \
	tests/test_growing_network_finite_section.py \
	tests/test_three_node_finite_section.py \
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

.PHONY: all paper figure diagnostic-data check clean

all: paper

figure: $(PAPER_FIGURES)

figures/connection-geometry.pdf: figures/connection_geometry.py
	$(PAPER_PYTHON) figures/connection_geometry.py --output $@

$(THREE_NODE_DATA): \
		../../experiments/three_node_finite_section_diagnostic.py \
		../../src/canard_control/three_node_finite_section.py
	cd ../.. && PYTHONPATH=src $(UV) run --extra numeric \
		python experiments/three_node_finite_section_diagnostic.py

$(GROWING_NETWORK_DATA): \
		../../experiments/growing_network_finite_section_diagnostic.py \
		../../src/canard_control/growing_network_finite_section.py
	cd ../.. && PYTHONPATH=src $(UV) run --extra numeric \
		python experiments/growing_network_finite_section_diagnostic.py

diagnostic-data: $(THREE_NODE_DATA) $(GROWING_NETWORK_DATA)

figures/three-node-finite-section.pdf: \
		figures/three_node_finite_section.py $(THREE_NODE_DATA) $(GROWING_NETWORK_DATA)
	$(PAPER_PYTHON) figures/three_node_finite_section.py \
		--data $(THREE_NODE_DATA) \
		--growing-data $(GROWING_NETWORK_DATA) --output $@

paper: $(PAPER_FIGURES)
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error main.tex

check:
	cd ../.. && $(UV) run --extra test pytest -q $(PAPER_A_TESTS)

clean:
	@if command -v $(LATEXMK) >/dev/null 2>&1; then \
		$(LATEXMK) -C main.tex; \
	fi
	$(RM) main.bbl supplement.aux supplement.bbl supplement.blg \
		supplement.fdb_latexmk supplement.fls supplement.log supplement.out \
		supplement.pdf supplement.synctex.gz
	@if [ -d build ]; then find build -type f -delete; fi
