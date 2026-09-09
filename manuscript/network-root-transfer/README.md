# Local fold matching in RFDE networks with constrained delayed coupling

This directory contains Paper A:

> **Local fold matching in RFDE networks with constrained delayed coupling**

## Main result and mechanism

Paper A constructs a two-dimensional locally invariant manifold of compatible
histories near a fold in a polynomial fast–slow RFDE network. Two specified
finite boundary-value problems define a matching function `D_N^fin` and a
unique nearby zero `nu_N^fin`. For `mu_N^fin = delta^2 nu_N^fin`, the main
theorem gives

```text
D_eta mu_N^fin(delta, eta)
  = delta^3 Lambda_N + O(delta^4 + delta^3 ||eta||),
```

with neighborhoods and bounds independent of the finite network size `N`
under common Dobrushin mixing, coefficient, and delay bounds. The matching
zero is selected by these finite boundary-value problems. It is not
identified with a global RFDE connection.

The delayed-coupling perturbations preserve the layer sum and satisfy
`pi_N^T Delta B_k = 0` at every delay. They leave the stationary projection of
the vector field unchanged at each full history, while changing the histories
themselves. Their first delay moment produces transverse forcing; the inverse
transverse generator and the heterogeneous quadratic coefficients give
`Lambda_N = r_N A_N^{-1} S_N`.

The supporting results compute a norm-optimal unrestricted two-delay right
inverse, the attainable range under prescribed matrix patterns, and uniform
bounds from Dobrushin contraction. Explicit growing families exhibit a
nonzero response with uniformly bounded perturbations and the loss of
uniformity for local cycles. Section 3 proves these results without repeating
their Section 2 statements.

## Conditional connection application

Section 5 specifies a smooth modification of the recovery equation away from
the fold. A heteroclinic conclusion additionally assumes actual hyperbolic
invariant-manifold sections and a scalar defining function `G` for their
intersection. For `E = G - D_N^fin`, the required comparison is

```text
|E| + |partial_nu E| <= C delta^2,
||D_eta E|| <= C delta^3.
```

Under these separate hypotheses, direct implicit differentiation gives the
same leading sensitivity for the modified equation's connection parameter.
The invariant-manifold and comparison estimates are not verified for that
modification. Different recovery laws can have different finite-`delta`
connection parameters. The paper does not prove a heteroclinic or maximal
canard for the unmodified recovery law or identify an experimental threshold.

## Source layout

- `main.tex`: front matter, six main sections, Appendix A, declarations, and
  bibliography in one PDF;
- `rewrite-sections/`: introduction, model and local results, delay-moment and
  Fredholm proofs, fold matching, conditional connection application, and
  discussion;
- `appendices/01-fold-details.tex`: detailed compatible-history graph and
  finite-interval matching estimates; the former connection Appendix B is
  removed from the revised manuscript;
- `figures/three_node_finite_section.py` and
  `figures/three-node-finite-section.pdf`: source and generated vector PDF for
  the article's single figure, Figure 1; the older connection-geometry figure
  is not an input to the normal paper build;
- `../../experiments/results/three_node_finite_section_diagnostic.json`:
  three-node finite-section illustration;
- `../../experiments/results/growing_network_finite_section_diagnostic.json`:
  growing-network illustration;
- `../../experiments/results/three_node_window_diagnostic.json`:
  independently varied fold parameter/window grid and solver refinements,
  reported in the numerical table;
- `CLAIM-MAP.md`: current statement-to-proof map and scope boundaries.

The immutable tags `paper-a-pre-rewrite-2026-09-02` and
`paper-a-dcds-submission-v1` preserve earlier versions. Neither describes the
present revision, which is not a tagged release.

## Build and checks

From this directory, run:

```sh
make paper
make check
```

`make paper` produces `main.pdf` with one appendix and one numerical figure.
`make check` runs `tests/test_paper_a_sources.py` to check active TeX inputs,
labels, citations, and graphics, together with the analytic-identity and
numerical regression tests listed in the Makefile. The source checks replace
the former prose-contract test; they do not freeze editorial wording or
verify the RFDE proofs.

Generate all three numerical data files with:

```sh
make diagnostic-data
```

Make only regenerates out-of-date targets. To force all data and the figure
from the repository root, run:

```sh
uv sync --extra numeric --extra paper
make -B -C manuscript/network-root-transfer diagnostic-data
make -C manuscript/network-root-transfer paper
```

Useful PDF checks are:

```sh
rg -n 'Warning|undefined|Overfull|Underfull' main.log
pdfinfo main.pdf
pdffonts main.pdf
```

## Numerical reproduction and scope

`../../uv.lock` records the Python dependencies. Each diagnostic JSON records
the Python, NumPy, and SciPy versions used for that run, together with source
hashes and solver settings. Regenerated artifacts may therefore report a
different Python patch version while retaining the locked numerical packages.

The diagnostics use a literal method of steps with Radau (`rtol=2e-9`,
`atol=2e-11`, `max_step=0.08`) and Brent roots (`xtol=rtol=2e-10`). The root
bracket starts with half-width `0.4` about the singular center and is doubled
at most four times. The new script
`../../experiments/three_node_window_diagnostic.py` crosses
`delta = 0.05, 0.02, 0.01` with window half-width `S = 3, 3.5, 4`, giving nine
points. Three points are repeated with `rtol=5e-10`, `atol=5e-12`,
`max_step=0.04`, and root tolerances `1e-11`; the largest change of the
normalized quotient is approximately `1.43e-8`. This is a floating-point
refinement comparison, not a rigorous error bound.

Figure 1 and the window table use prescribed incoming histories and an
outgoing-section condition. They illustrate the coefficient's sign, scale,
network-size persistence, and dependence on the finite window. Their zeros
are not those of `D_N^fin`, and the computations neither establish a
heteroclinic connection nor verify the global hypotheses. The analytic
results do not rely on these diagnostics.
