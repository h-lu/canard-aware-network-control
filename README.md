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

The DCDS submission source is preserved at the immutable tag and release
`paper-a-dcds-submission-v1`.

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

### Numerical reproduction details

The locked Python environment is recorded in `uv.lock`.  The reference JSON
files were generated with Python 3.14.4, NumPy 2.5.2, and SciPy 1.18.1; each
JSON file also records these versions and SHA-256 hashes of its numerical
source files.  Both diagnostics use a literal method of steps with
`scipy.integrate.solve_ivp(method="Radau", dense_output=True)`, relative
tolerance `2e-9`, absolute tolerance `2e-11`, and maximum step `0.08`.
The scalar outgoing-section zero is found with Brent's method
(`scipy.optimize.root_scalar(method="brentq")`) using absolute and relative
root tolerances `2e-10`.  The full data and Figure 2 can be regenerated from
the repository root by running

```sh
uv sync --extra numeric --extra paper
make -B -C manuscript/network-root-transfer paper
```

The root bracket starts with half-width `0.4` about the singular center and is
doubled at most four times.  The three-node refinement additionally uses
`rtol=5e-10`, `atol=5e-12`, and `max_step=0.04`.
The three-node sweep uses
`(delta,S)=(0.12,2.5),(0.08,2.75),(0.05,3),(0.02,3.5),(0.01,4)`, and the
growing-family sweep uses `delta=0.02`, `S=3.5`, and
`N=3,5,9,17,33`.  In both cases the centered perturbation step is `0.04`.

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
