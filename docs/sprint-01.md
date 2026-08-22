# Sprint 01: analytical feasibility before scale-up

Window: **2026-08-22 to 2026-09-04**

Goal: decide whether the flagship theorem chain is viable on delayed van der Pol and an exact two-module network before investing in large simulations.

## Work packages

### WP1 -- Freeze the mathematical object ([#1](https://github.com/h-lu/canard-aware-network-control/issues/1))

- [x] Choose a section-defined observable splitting as the threshold.
- [x] Freeze the weak-coupling/scaled-delay regime.
- [x] Declare graphons and arbitrary sparse networks out of first-paper scope.
- [ ] Write the precise entry data, section, orientation, and invariant-manifold selections.
- [ ] State the compact parameter wedge and all uniformity requirements.

Acceptance: two independent implementations return the same delayed van der Pol threshold to the predicted numerical tolerance.

### WP2 -- Exact two-module reduction ([#2](https://github.com/h-lu/canard-aware-network-control/issues/2))

- [ ] Fix the weight normalization and equitable-partition notation.
- [ ] Prove invariance of the block-synchronous history space.
- [ ] Derive the exact two-module RFDE.
- [ ] Construct one perturbation family with a tunable residual norm.

Acceptance: full and reduced trajectories agree at roundoff for block-synchronous histories when the residual is zero.

### WP3 -- Delay-moment derivation ([#3](https://github.com/h-lu/canard-aware-network-control/issues/3))

- [ ] Reproduce the published delayed van der Pol blow-up scaling.
- [ ] Expand the translated history to the first three candidate orders.
- [ ] Project each term onto the chosen observable splitting.
- [ ] Identify the first nonzero weighted moment; record all cancellations.
- [ ] Cross-check by symbolic algebra and high-precision continuation.

Acceptance: coefficient and order agree across the two derivations, without regression fitting.

### WP4 -- Transfer lemma ([#4](https://github.com/h-lu/canard-aware-network-control/issues/4))

- [ ] Select the delayed coupling operator norm.
- [ ] Bound the manifold/splitting perturbation in that norm.
- [ ] Apply a quantitative root perturbation lemma.
- [ ] Test first-order threshold shift on held-out residual directions.

Acceptance: normalized remainder is second order over at least one decade before numerical error dominates.

### WP5 -- Control rank pilot ([#5](https://github.com/h-lu/canard-aware-network-control/issues/5))

- [ ] Specify admissible linear, nonlinear, and delay-moment actuators.
- [ ] Derive adjoint/sensitivity equations for \(F\), \(R_h\), and \(\Delta_c^h\).
- [ ] Compute singular values and actuator-condition maps.
- [ ] Compare against one- and two-actuator no-go baselines.

Acceptance: either exhibit an open full-rank region or record a rigorous local obstruction and redesign the actuator set.

### WP6 -- Numerical certificate skeleton ([#6](https://github.com/h-lu/canard-aware-network-control/issues/6))

- [ ] Separate RK/collocation, history interpolation, reduction, and root errors.
- [ ] Add the fold-local RK chain-tree defect to method metadata.
- [ ] Implement nested refinement and an uncertainty budget.
- [ ] Reject results whose uncertainty exceeds the claimed threshold shift.

Acceptance: a manufactured delayed problem recovers its known threshold and observed order inside the certificate.

## Calendar

| Date | Primary output | Decision |
|---|---|---|
| Aug 22--23 | literature map, scope, definitions | novelty and scope freeze |
| Aug 24--26 | exact reduction + symbolic blow-up notebook | first nonzero moment |
| Aug 27--29 | transfer lemma draft + residual experiment | theorem viability |
| Aug 30--Sep 1 | three-coordinate sensitivity pilot | full-rank/no-go |
| Sep 2--3 | numerical error budget + refinement tests | certification viability |
| Sep 4 | internal proof/claim audit | continue, narrow, or redesign |

## Reproducibility rule

Every figure must be generated from a committed configuration and machine-readable result summary. Raw large trajectories remain outside Git; checksums and generation commands are committed. No device is assigned by this plan--the first sprint is CPU-scale and hardware placement is a later explicit decision.
