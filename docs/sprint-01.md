# Sprint 01: Lin-gap feasibility before scale-up

Window: **2026-08-22 to 2026-09-04**

Goal: decide whether one RFDE canard-root transfer theorem is viable before investing in large simulations or general rank-\(r\) claims.

## WP1 -- Define the scalar Lin gap ([#1](https://github.com/h-lu/canard-aware-network-control/issues/1))

- [ ] Fix the blown-up history space, entry/exit data, matching section, and phase condition.
- [ ] Write the RFDE Lin boundary-value operator.
- [ ] Determine its Fredholm index after the phase condition.
- [ ] Verify that the relevant cokernel is one-dimensional.
- [ ] Define the adjoint gap and prove coordinate/complement independence.
- [ ] Separate a geometric maximal-canard root from an output-event threshold.

Acceptance: a mathematically defined scalar gap, not a projected difference between two sets.

## WP2 -- Build the exact reference and audit transverse modes ([#2](https://github.com/h-lu/canard-aware-network-control/issues/2))

- [ ] Prove the common-row-measure synchronous RFDE closure.
- [ ] Write the exact two-module delayed FHN reference system.
- [ ] Derive the transverse delayed variational/Lin operator.
- [ ] Construct or bound its Green/Fredholm inverse \(G_\perp(\varepsilon)\).
- [ ] Test whether \(O(\varepsilon)\) coupling leaves additional fold-critical directions.
- [ ] If the inverse grows too rapidly, restrict the residual scaling or reference class.

Acceptance: an explicit \(G_\perp(\varepsilon)\) estimate or a documented falsification that narrows Theorem A.

## WP3 -- Complete Proposition B ([#3](https://github.com/h-lu/canard-aware-network-control/issues/3))

- [x] Reproduce the delayed van der Pol blow-up scaling.
- [x] Verify formally \(\nu_0=-1/8\) and \(\nu_1=K\Theta/8\).
- [x] Derive the formal \(Km_1/8\) coefficient for the common-row-measure class.
- [ ] Put the expansion inside the Lin-gap formulation.
- [ ] Prove an \(O(\varepsilon^2)\) remainder uniform in \(N\) and the declared measure class.
- [ ] Verify that \(m_2\) changes the graph but cancels from the parameter at this order.
- [ ] Derive the two-module \(M_1^{(2)}\) term under an explicit leading mode-closure condition, or expose the extra transverse resolvent term.

Acceptance: a theorem-level remainder; symbolic coefficient agreement alone does not pass.

## WP4 -- Prove Theorem A ([#4](https://github.com/h-lu/canard-aware-network-control/issues/4))

- [ ] Choose a residual norm that controls delay translation on the strong history space.
- [ ] Prove \(C^2\) dependence of the Lin problem on weights, delay measures, and node parameters.
- [ ] Solve the range equation using \(G_\perp(\varepsilon)\).
- [ ] Derive the first-variation functional and quadratic remainder.
- [ ] Transfer the simple root with an explicit \(m_\varepsilon\) denominator.
- [ ] State the joint limit needed to resolve the \(O(\varepsilon^{3/2})\) moment term.

Acceptance: a complete scoped proof or a precise obstruction reducing the theorem to the exact invariant class.

## WP5 -- Establish Corollary C ([#5](https://github.com/h-lu/canard-aware-network-control/issues/5))

- [ ] Freeze the two-module FHN equations, observable, parameter box, and linear/cubic/delay-deformation actuators.
- [ ] Prove periodic-branch hyperbolicity and unique nondegenerate output extrema.
- [ ] Derive the frequency, amplitude, and Lin-root sensitivities.
- [ ] Factor the response determinant into the \((F,R_h)\) block and the safety Schur complement.
- [ ] Prove \(\sigma_{\min}(D_uQ)\ge c_Q(\varepsilon)>0\) on a nonempty region.
- [ ] Derive a quantitative local inverse radius.
- [ ] Prove a structural one-/two-actuator rank obstruction if available.

Acceptance: a proved or rigorously enclosed lower bound; a plotted nonzero determinant alone is insufficient.

## WP6 -- Verification module ([#6](https://github.com/h-lu/canard-aware-network-control/issues/6))

- [ ] Implement two independent RFDE root calculations.
- [ ] Enclose the Lin-gap residual and derivative denominator on a root interval.
- [ ] Separate physical delay, full/reduced transfer, and numerical errors.
- [ ] Test the first variation on held-out residual directions.
- [ ] Run delay-moment, trajectory-close/threshold-wrong, and actuator-count negative controls.
- [ ] Reject every claimed effect smaller than its uncertainty.

Acceptance: all four paper claims are resolved within a reproducible uncertainty budget.

## Calendar and decision gates

| Date | Primary output | Decision |
|---|---|---|
| Aug 22--24 | Lin operator, phase condition, and scalar gap | definition gate |
| Aug 25--27 | exact reference and transverse inverse audit | theorem feasibility gate |
| Aug 28--30 | first-moment uniform-remainder attempt | proposition gate |
| Aug 31--Sep 2 | Lyapunov--Schmidt/root-transfer proof | main theorem gate |
| Sep 3 | concrete FHN sensitivity pilot | corollary gate |
| Sep 4 | proof/claim audit and next-sprint decision | continue, narrow, or redesign |

## Reproducibility rule

Every figure is generated from a committed configuration and machine-readable summary. Large trajectories remain outside Git; checksums and generation commands are committed. No device is assigned by this plan. The first sprint is a CPU-scale analytical and small-system feasibility audit.
