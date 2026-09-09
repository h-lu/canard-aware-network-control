# Canard-aware network dynamics and control

This repository contains three separate research programs for delayed
fast--slow systems. They share code and references but are not presented as
one paper.

| Workspace | Role | Status |
| --- | --- | --- |
| [`manuscript/network-root-transfer`](manuscript/network-root-transfer) | Paper A: local fold matching and sensitivity to constrained delayed coupling | Local major revision; single PDF |
| [`manuscript/pulse-threshold`](manuscript/pulse-threshold) | Paper B: stable-manifold pulse threshold in a delayed FitzHugh--Nagumo equation | Research draft; proof chain incomplete |
| [`manuscript/rfde-methods-notes`](manuscript/rfde-methods-notes) | Paper C: regularity and event maps for RFDEs | Working notes; independent novelty still under review |

## Paper A

**Local fold matching in RFDE networks with constrained delayed coupling**
constructs a two-dimensional locally invariant manifold of compatible RFDE
histories near a fold. Two finite boundary-value problems define the matching
function `D_N^fin`, its unique nearby zero `nu_N^fin`, and
`mu_N^fin = delta^2 nu_N^fin`. The first main theorem proves

```text
D_eta mu_N^fin(delta, eta)
  = delta^3 Lambda_N + O(delta^4 + delta^3 ||eta||),
```

uniformly over finite networks with common Dobrushin mixing, coefficient, and
delay bounds. This zero belongs to the specified finite matching problem.

The constrained delayed-coupling perturbations preserve the layer sum and
have zero stationary row at every delay. Their direct contribution to the
projected vector field vanishes at each full history, while their effect on
transverse histories returns through heterogeneous node nonlinearities. The
paper computes that response from the first delay moment, the transverse
inverse, and a Gaussian Fredholm pairing. Supporting results give the exact
range under prescribed matrix patterns, norm-optimal unrestricted right
inverses, and growing-family examples.

The heteroclinic application in Section 5 remains conditional. It requires
actual invariant-manifold sections and a scalar defining function `G`, with
`E = G - D_N^fin` satisfying `|E| + |partial_nu E| <= C delta^2` and
`||D_eta E|| <= C delta^3`. These global estimates are not verified for the
specified modified recovery equation. The paper does not prove a maximal
canard for the unmodified recovery law or identify an experimental threshold.

The immutable tags `paper-a-pre-rewrite-2026-09-02` and
`paper-a-dcds-submission-v1` preserve earlier manuscript versions. The present
revision is not a tagged release.

## Build and verify Paper A

Requirements are a recent TeX Live installation, Python 3.11 or newer, and
[`uv`](https://docs.astral.sh/uv/). Run:

```sh
cd manuscript/network-root-transfer
make paper
make check
```

The normal build produces `main.pdf` with Appendix A and one numerical figure
(Figure 1); it no longer includes the connection Appendix B or the
connection-geometry figure. The test target checks source dependencies,
labels, citations, and graphics through `tests/test_paper_a_sources.py`, plus
analytic identities and numerical regressions. These checks do not verify
the RFDE proofs or freeze editorial wording.

### Numerical reproduction details

`uv.lock` records the Python dependencies. Each diagnostic JSON records the
Python, NumPy, and SciPy versions used for that run, together with its solver
settings and source hashes. Regenerated artifacts may therefore report a
different Python patch version while retaining the locked numerical packages.

The diagnostics use a literal method of steps with Radau, `rtol=2e-9`,
`atol=2e-11`, and `max_step=0.08`; Brent root finding uses `xtol=rtol=2e-10`.
The root bracket starts with half-width `0.4` about the singular center and is
doubled at most four times. The original three-node sweep uses
`(delta,S)=(0.12,2.5),(0.08,2.75),(0.05,3),(0.02,3.5),(0.01,4)`, and the
growing-family sweep uses `delta=0.02`, `S=3.5`, and `N=3,5,9,17,33`.
The centered perturbation step is `0.04`.

`experiments/three_node_window_diagnostic.py` varies `delta=0.05,0.02,0.01`
and `S=3,3.5,4` independently on a nine-point grid. Three tighter solver
repeats use `rtol=5e-10`, `atol=5e-12`, `max_step=0.04`, and root tolerances
`1e-11`; their largest normalized-quotient change is about `1.43e-8`. These
are floating-point diagnostics of finite-window and solver effects, not
rigorous error bounds. Neither Figure 1 nor the window table computes
`D_N^fin` or a heteroclinic connection.

To force regeneration of all three data files and rebuild the figure/PDF
from the repository root, run:

```sh
uv sync --extra numeric --extra paper
make -B -C manuscript/network-root-transfer diagnostic-data
make -C manuscript/network-root-transfer paper
```

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
`experiments/three_node_finite_section_diagnostic.py`,
`experiments/growing_network_finite_section_diagnostic.py`, and
`experiments/three_node_window_diagnostic.py`; none is used as a proof of the
global hypotheses.
