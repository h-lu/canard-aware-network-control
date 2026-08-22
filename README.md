# Canard-threshold transfer under weak delayed feedback

Research repository for one flagship paper:

> **Canard-threshold transfer under weak delayed feedback in slow--fast networks, with a concrete frequency--amplitude--safety corollary**

## Central question

When a biological network with weak delayed feedback is close to a canard explosion, can a reduced RFDE predict the **manifold-matching threshold** of the full finite network with a controlled error?

The first paper has one mathematical spine:

1. formulate the delayed canard as a one-dimensional Lin matching gap;
2. prove the gap and its simple root respond differentiably to finite-network residuals;
3. calculate the leading topology-weighted delay functional in a controlled model class.

A two-module delayed FitzHugh--Nagumo control result and residual-based computation support this theorem. They are not parallel novelty claims.

## Frozen first-paper scope

- finite networks near an exact equitable two-module skeleton whose one-gap Fredholm hypothesis is verified rather than inferred from equitability;
- weak delayed feedback \(J=O(\varepsilon)\) and scaled delays \(\tau_{ij}=\Theta_{ij}/\sqrt{\varepsilon}\), with \(\Theta_{ij}\) in a compact set;
- a fixed instantaneous synchronization scaffold in the concrete FHN control benchmark; it vanishes on the collective history and is not an actuator;
- a fixed entry/exit formulation, phase condition, and one-dimensional Lin gap after all transverse matching conditions are imposed;
- a compatible strong history space or delay-measure norm in which delay translations are controlled;
- an explicit transverse RFDE Green/Fredholm inverse bound \(G_\perp(\sqrt\varepsilon)\), rather than adjacency spectral gap alone;
- delayed van der Pol as the analytic calibration model;
- a two-module delayed FitzHugh--Nagumo network as the biological benchmark;
- three design coordinates: linear feedback gain, nonlinear feedback gain, and a realizable weighted delay moment.

General rank-\(r\) closure, graphon limits, arbitrary sparse nonnormal networks, strong delays, and nonsmooth all-node thresholds are extensions, not claims of the first paper.

## One theorem, one proposition, one corollary

1. **Main theorem -- RFDE Lin-gap threshold transfer.** Near an exact reference network, the full-network canard matching root has a first-order structural response and a controlled second-order remainder. The constants expose \(G_\perp(\sqrt\varepsilon)\), root transversality, and the chosen residual norm.
2. **Explicit proposition -- first delay moment.** Use the common-row-measure delayed van der Pol class as calibration, then prove the two-module \(M_1^{(2)}\) coefficient under an explicit mode-closure condition, with a uniform remainder.
3. **Concrete corollary -- two-module FHN control.** For three specified admissible actuators, derive the response matrix for frequency, squared amplitude, and canard safety margin and prove a nonzero singular-value lower bound on a declared parameter region.
4. **Validation module.** Enclose the Lin-gap root error by residual and refinement bounds; reuse the earlier ODE/RK threshold result only as a cited baseline.

These are research targets, not established results. The scalar and common-row-measure coefficients currently have formal polynomial-solvability checks, but not the uniform remainder required by the proposition. Precise statements and falsification gates are in [docs/scope-and-theorems.md](docs/scope-and-theorems.md).

## First feasibility result

The definition gate has produced two substantive corrections:

1. after phase fixing, the one-gap Lin linearization has Fredholm index
   \(-1\), zero kernel, and one-dimensional cokernel; adjoining the scalar Lin
   jump gives the invertible index-zero operator;
2. two identical modules coupled only through \(O(\varepsilon)\) delayed
   diffusion inherit a repeated node-canard degeneracy at \(\varepsilon=0\).
   In the canonical symmetric inner problem the first relative splitting
   projection cancels and the formal second coefficient is nonzero, predicting
   a potentially severe \(G_\perp=O(\varepsilon^{-1})\) conditioning.

Accordingly, the weak-only class is a negative control or a narrow
joint-limit theorem. The concrete FHN control corollary uses a fixed
instantaneous transverse scaffold while keeping all three delayed actuators
weak. Neither the Fredholm upper bound nor the uniform remainder is yet
claimed proved.

## Repository map

- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/scope-and-theorems.md` -- model, Lin-gap definition, main theorem specification, and stop/go gates;
- `docs/lin-gap-feasibility.md` -- full-history BVP, correct Fredholm index, augmented gap, and open proof obligations;
- `docs/two-module-reference.md` -- frozen FHN benchmark and weak-only transverse obstruction;
- `docs/derivation-leading-moment.md` -- formally checked scalar/common-row-measure coefficients and the missing remainder obligations;
- `docs/sprint-01.md` -- first two-week execution plan linked to GitHub issues;
- `manuscript/outline.md` -- single-paper narrative, figures, and evidence standard;
- `references/references.bib` -- curated and deduplicated primary references;
- `src/canard_control/transverse_modes.py` -- executable weak-only inner splitting audit;
- `src/canard_control/reference_fhn.py` -- exact algebra for the scaffolded two-module benchmark;
- `tests/`, `experiments/` -- verification and reproducible experiments.

## Project tracking

- [Flagship-paper epic](https://github.com/h-lu/canard-aware-network-control/issues/9)
- [Milestone: Flagship paper v1](https://github.com/h-lu/canard-aware-network-control/milestone/1)

## Immediate decision gate

Before large simulations, the project must prove the frozen-model augmented Lin operator has one cokernel direction and obtain a usable transverse inverse bound \(G_\perp(\sqrt\varepsilon)\). The definition itself is now fixed. The first-delay coefficient and root transversality are then checked inside that formulation. Failure narrows the theorem to the exact invariant class before any expensive computation.
