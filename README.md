# Canard-aware network dynamics and control

This repository contains three separate research programs for delayed
fast--slow systems. They share code and references but are not presented as
one paper.

| Workspace | Role | Status |
| --- | --- | --- |
| [`manuscript/network-root-transfer`](manuscript/network-root-transfer) | Paper A: a Fredholm formula for constrained delayed-coupling perturbations | Rewritten single-PDF article |
| [`manuscript/pulse-threshold`](manuscript/pulse-threshold) | Paper B: stable-manifold pulse threshold in a delayed FitzHugh--Nagumo equation | Research draft; proof chain incomplete |
| [`manuscript/rfde-methods-notes`](manuscript/rfde-methods-notes) | Paper C: regularity and event maps for RFDEs | Working notes; independent novelty still under review |

## Paper A

Paper A studies finite networks of retarded functional differential
equations with a row-stochastic instantaneous coupling and additional
feedback distributed among several delays. A perturbation that preserves
the sum of the delayed-coupling matrices and has zero
stationary row leaves the stationary projection of the vector field
unchanged at every history. Nevertheless, two distinct delay locations
generate every transverse first-order forcing direction. The paper gives an
explicit right inverse, dimension-independent bounds, and the resulting
bounded linear functional from the Fredholm solvability condition.

For a prescribed linear matrix pattern, the paper identifies the exact range
of the first-moment map and gives a fixed-support realization. It also
constructs a local invariant graph of compatible RFDE histories for the
polynomial fast--slow network, computes the coefficient in a finite-interval
matching function, and exhibits a growing family whose nonzero coefficient is
independent of network size. Applying that coefficient to a heteroclinic
orbit in a specified modified equation is a separate, conditional result: it
requires uniform invariant-manifold sections and a `C^1` comparison estimate.
That global verification is not claimed here. The
paper neither proves a maximal canard for the unmodified recovery law nor
identifies an experimental threshold.

The manuscript preceding the rewrite is preserved at the immutable tag
`paper-a-pre-rewrite-2026-09-02` and its associated GitHub release.

## Build and verify Paper A

Requirements are a recent TeX Live installation, Python 3.11 or newer, and
[`uv`](https://docs.astral.sh/uv/). Run:

```sh
cd manuscript/network-root-transfer
make paper
make check
```

The build regenerates the vector figures and produces the single submission
file `main.pdf`, including both proof appendices. The test target checks the public theorem architecture and
the analytic identities used by Paper A, together with lightweight
regression checks for the illustrative three-node and growing-network
calculations; it is not a
substitute for the proofs.

## Repository map

- [`src/canard_control`](src/canard_control): symbolic and analytic modules;
- [`tests`](tests): regression and manuscript-contract tests;
- [`experiments`](experiments): reproducible exploratory calculations;
- [`docs`](docs): research records and literature maps;
- [`references/references.bib`](references/references.bib): shared bibliography;
- [`manuscript`](manuscript): current and historical manuscript workspaces.

The closest-literature summaries are in
[`docs/literature-map.md`](docs/literature-map.md) and
[`docs/physical-root-literature-audit.md`](docs/physical-root-literature-audit.md).
Historical numerical artifacts retain their original environments and should
not be interpreted as inputs to the analytic theorem in Paper A. The current
finite-section diagnostics are reproducible from
`experiments/three_node_finite_section_diagnostic.py` and
`experiments/growing_network_finite_section_diagnostic.py`; neither is used as
a proof of the global hypotheses.
