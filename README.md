# Canard-aware network control

Research repository for one flagship paper:

> **Observable-projected canard-threshold transfer and frequency--amplitude--safety control in delayed slow--fast biological networks**

## Central question

When a weakly coupled delayed biological network is close to a canard explosion, can a reduced model predict an **observable-projected pulse threshold** of the full network, and can frequency, amplitude, and the distance to that threshold be assigned independently?

The project joins three problems that are usually treated separately:

1. local canard asymptotics for delayed slow--fast systems;
2. topology-aware reduction and threshold transfer in heterogeneous networks;
3. local inverse control of frequency, amplitude, and a safety margin.

## Frozen first-paper scope

- finite networks with an exact rank-\(r\)/equitable block skeleton plus a controlled residual;
- weak coupling \(J=O(\varepsilon)\) and scaled delays \(\tau_{ij}=\Theta_{ij}/\sqrt{\varepsilon}\), with \(\Theta_{ij}\) in a compact set;
- a specified smooth Perron- or module-weighted observable;
- a section-defined observable-projected canard-splitting threshold, not an informal visual jump point;
- delayed van der Pol as the analytic calibration model;
- a two-module delayed FitzHugh--Nagumo network as the biological benchmark;
- three design coordinates: linear feedback gain, nonlinear feedback gain, and a realizable weighted delay moment.

Graphon limits, arbitrary sparse nonnormal networks, strong delays, and an all-node threshold are extensions, not claims of the first paper.

## Planned theorem chain

1. **Exact reduction.** Equitable weights and block-constant delays give an invariant block-synchronous RFDE and an exact \(r\)-module delayed reduction.
2. **Threshold transfer.** A small network residual perturbs the section splitting, yielding a first-order shift of the observable-projected canard threshold.
3. **Delay-moment selection.** Blow-up identifies which topology-weighted delay moments enter each asymptotic order.
4. **Three-coordinate control.** A full-rank response map for frequency, squared amplitude, and safety margin gives local independent assignment; rank loss gives a no-go criterion.
5. **Numerical certificate.** The computed threshold carries a decomposed error bound for time stepping, history interpolation, network reduction, and root residual.

These are research targets, not established results. Precise candidate statements and falsification gates are in [docs/scope-and-theorems.md](docs/scope-and-theorems.md).

## Repository map

- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/scope-and-theorems.md` -- model, definitions, candidate theorem ladder, and stop/go gates;
- `docs/sprint-01.md` -- first two-week execution plan linked to GitHub issues;
- `manuscript/outline.md` -- single-paper narrative, figures, and evidence standard;
- `references/references.bib` -- curated and deduplicated primary references;
- `src/`, `tests/`, `experiments/` -- implementation and reproducible experiments.

## Project tracking

- [Flagship-paper epic](https://github.com/h-lu/canard-aware-network-control/issues/9)
- [Milestone: Flagship paper v1](https://github.com/h-lu/canard-aware-network-control/milestone/1)

## Immediate decision gate

Before large simulations, the project must pass a symbolic calibration test on the delayed van der Pol model: the first nonzero delay-moment contribution and the threshold transversality denominator must both be derived and independently checked. Failure narrows the claim before any expensive computation.
