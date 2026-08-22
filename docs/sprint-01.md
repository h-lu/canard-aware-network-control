# Sprint 01: Lin-gap feasibility before scale-up

Window: **2026-08-22 to 2026-09-04**

Goal: decide whether one RFDE canard-root transfer theorem is viable before investing in large simulations or general rank-\(r\) claims.

## WP1 -- Define the reference gap and full-network Lin operator ([#1](https://github.com/h-lu/canard-aware-network-control/issues/1))

- [x] Fix the \(\mathbb R^4\) reference history space, candidate entry/exit data, matching section, and phase condition.
- [x] Write the \(\mathbb R^4\) reference full-history RFDE Lin boundary-value template.
- [ ] Construct the full \(2N\)-state operator and compatible entry/exit bundles for synchrony-breaking residuals.
- [x] Correct the required post-phase index to \(-1\) and define the index-zero jump augmentation.
- [ ] Verify that the relevant cokernel is one-dimensional.
- [x] Define the adjoint gap and its normalization-independent root response.
- [ ] Prove coordinate/complement independence for the frozen model and norms.
- [x] Separate a geometric maximal-canard root from an output-event threshold.
- [ ] Construct the backward-extendible repelling piece on the RFDE center/solution manifold.

Acceptance: a mathematically defined full-network scalar gap, not a projected difference between two sets or only a reduced \(\mathbb R^4\) template.

## WP2 -- Build the exact reference and audit transverse modes ([#2](https://github.com/h-lu/canard-aware-network-control/issues/2))

- [x] Prove the common-row-measure synchronous RFDE closure by substitution.
- [x] Write the exact two-module delayed FHN reference system.
- [x] Derive the weak-only fold-scaled transverse variational operator.
- [ ] Construct or bound its Green/Fredholm inverse \(G_\perp(\delta)\), \(\delta=\sqrt\varepsilon\).
- [x] Show that \(O(\varepsilon)\) delayed coupling leaves repeated fold-critical directions at \(\varepsilon=0\).
- [x] Verify zero first and nonzero formal second inner splitting coefficients for the symmetric whole-line diagnostic.
- [x] Implement the finite-interval singular-value sweep and verify that symmetric versus asymmetric endpoint choices change the observed weak-only exponent.
- [x] Restrict the weak-only class to a negative control/narrow joint limit and freeze a scaffolded FHN control benchmark.
- [x] Show that the scaffold leaves \(N-1\) recovery center directions at \(\varepsilon=0\); a single fast fold is not a one-cokernel proof.
- [ ] Prove the one-cokernel property and bound \(G_\perp(\delta)\) for the scaffolded Lin BVP.

Acceptance: an explicit \(G_\perp(\delta)\) estimate or a documented falsification that narrows Theorem A.

## WP3 -- Complete Proposition B ([#3](https://github.com/h-lu/canard-aware-network-control/issues/3))

- [x] Reproduce the delayed van der Pol blow-up scaling.
- [x] Verify formally \(\nu_0=-1/8\) and \(\nu_1=K\Theta/8\).
- [x] Derive the formal \(Km_1/8\) coefficient for the common-row-measure class.
- [ ] Put the expansion inside the Lin-gap formulation.
- [ ] Prove an \(O(\varepsilon^2)\) remainder uniform in \(N\) and the declared measure class.
- [ ] Verify that \(m_2\) changes the graph but cancels from the parameter at this order.
- [x] Prove the exact layerwise mode-closure criterion.
- [x] Construct a positive two-delay family with fixed total gain and fixed projected \(M_1^{(2)}\) but nonzero transverse forcing.
- [x] Verify a nonzero FHN nonlinear return coefficient for that forcing.
- [x] Prove the Perron no-go mechanism for positive-mode closure in nonnegative receiver-self diffusion.
- [ ] Derive the dynamic-adjoint transverse functional \(\mathcal J_{\perp,\delta}\), its coefficient, and its singular-limit scaling.

Acceptance: a theorem-level remainder; symbolic coefficient agreement alone does not pass.

## WP4 -- Prove Theorem A ([#4](https://github.com/h-lu/canard-aware-network-control/issues/4))

- [ ] Choose a residual norm that controls delay translation on the strong history space.
- [ ] Prove \(C^2\) dependence of the Lin problem on weights, delay measures, and node parameters.
- [ ] Solve the range equation using \(G_\perp(\delta)\).
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
| Aug 22--24 | Lin operator, phase condition, and scalar gap | specification passed; Fredholm proof open |
| Aug 25--27 | exact reference and transverse inverse audit | weak-only uniform gate failed; scaffolded reference frozen |
| Aug 28--30 | first-moment uniform-remainder attempt | proposition gate |
| Aug 31--Sep 2 | Lyapunov--Schmidt/root-transfer proof | main theorem gate |
| Sep 3 | concrete FHN sensitivity pilot | corollary gate |
| Sep 4 | proof/claim audit and next-sprint decision | continue, narrow, or redesign |

## Reproducibility rule

Every figure is generated from a committed configuration and machine-readable summary. Large trajectories remain outside Git; checksums and generation commands are committed. No device is assigned by this plan. The first sprint is a CPU-scale analytical and small-system feasibility audit.
