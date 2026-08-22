# Canard-threshold transfer in delayed networks

Research repository for one flagship paper:

> **Canard-threshold transfer in weakly delayed slow--fast networks, with a concrete frequency--amplitude--safety corollary**

## Central question

When a weakly coupled delayed biological network is close to a canard explosion, can a reduced RFDE predict the **manifold-matching threshold** of the full finite network with a controlled error?

The first paper has one mathematical spine:

1. formulate the delayed canard as a one-dimensional Lin matching gap;
2. prove the gap and its simple root respond differentiably to finite-network residuals;
3. calculate the leading topology-weighted delay functional in a controlled model class.

A two-module delayed FitzHugh--Nagumo control result and residual-based computation support this theorem. They are not parallel novelty claims.

## Frozen first-paper scope

- finite networks near an exact equitable two-module skeleton with one simple collective canard direction;
- weak coupling \(J=O(\varepsilon)\) and scaled delays \(\tau_{ij}=\Theta_{ij}/\sqrt{\varepsilon}\), with \(\Theta_{ij}\) in a compact set;
- a fixed entry/exit formulation, phase condition, and one-dimensional Lin gap after all transverse matching conditions are imposed;
- a compatible strong history space or delay-measure norm in which delay translations are controlled;
- an explicit transverse RFDE Green/Fredholm inverse bound \(G_\perp(\varepsilon)\), rather than adjacency spectral gap alone;
- delayed van der Pol as the analytic calibration model;
- a two-module delayed FitzHugh--Nagumo network as the biological benchmark;
- three design coordinates: linear feedback gain, nonlinear feedback gain, and a realizable weighted delay moment.

General rank-\(r\) closure, graphon limits, arbitrary sparse nonnormal networks, strong delays, and nonsmooth all-node thresholds are extensions, not claims of the first paper.

## One theorem, one proposition, one corollary

1. **Main theorem -- RFDE Lin-gap threshold transfer.** Near an exact reference network, the full-network canard matching root has a first-order structural response and a controlled second-order remainder. The constants expose \(G_\perp(\varepsilon)\), root transversality, and the chosen residual norm.
2. **Explicit proposition -- first delay moment.** Use the common-row-measure delayed van der Pol class as calibration, then prove the two-module \(M_1^{(2)}\) coefficient under an explicit mode-closure condition, with a uniform remainder.
3. **Concrete corollary -- two-module FHN control.** For three specified admissible actuators, derive the response matrix for frequency, squared amplitude, and canard safety margin and prove a nonzero singular-value lower bound on a declared parameter region.
4. **Validation module.** Enclose the Lin-gap root error by residual and refinement bounds; reuse the earlier ODE/RK threshold result only as a cited baseline.

These are research targets, not established results. The scalar and common-row-measure coefficients currently have formal polynomial-solvability checks, but not the uniform remainder required by the proposition. Precise statements and falsification gates are in [docs/scope-and-theorems.md](docs/scope-and-theorems.md).

## Repository map

- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/scope-and-theorems.md` -- model, Lin-gap definition, main theorem specification, and stop/go gates;
- `docs/derivation-leading-moment.md` -- formally checked scalar/common-row-measure coefficients and the missing remainder obligations;
- `docs/sprint-01.md` -- first two-week execution plan linked to GitHub issues;
- `manuscript/outline.md` -- single-paper narrative, figures, and evidence standard;
- `references/references.bib` -- curated and deduplicated primary references;
- `src/`, `tests/`, `experiments/` -- implementation and reproducible experiments.

## Project tracking

- [Flagship-paper epic](https://github.com/h-lu/canard-aware-network-control/issues/9)
- [Milestone: Flagship paper v1](https://github.com/h-lu/canard-aware-network-control/milestone/1)

## Immediate decision gate

Before large simulations, the project must define a well-posed one-dimensional Lin problem and obtain a usable transverse inverse bound \(G_\perp(\varepsilon)\). The first-delay coefficient and root transversality are then checked inside that formulation. Failure narrows the theorem to the exact invariant class before any expensive computation.
