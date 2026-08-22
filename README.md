# Transverse delay organization and canard thresholds

Research repository for one proof-first flagship paper:

> **Transverse Delay Effects on a Canard Threshold in a Two-Module
> FitzHugh--Nagumo System**

The current proof-first submission design is
[docs/flagship-research-design.md](docs/flagship-research-design.md). It
freezes a two-module transverse-delay theorem as the minimum publishable
core. General finite-network transfer and three-coordinate control are
promotion targets: they enter the same paper only after the core RFDE
geometry and remainder are proved.

## Central question

Can two weakly delayed FitzHugh--Nagumo modules have the same total delayed
gain and the same delay measure seen by the critical projection, yet have
different local canard thresholds because the delay forcing passes through a
stable transverse mode?

The first paper has one mathematical spine:

1. freeze one two-module, two-delay RFDE and prove its exact singular spectrum;
2. construct its two-dimensional invariant history manifold and
   complete-history embedding;
3. calculate the transverse nonlinear return and prove the resulting simple
   local canard root with a uniform remainder.

The broader finite-network Lin transfer and frequency--amplitude--safety
control programs remain in the repository as conditional promotions. They
are not assumptions or parallel novelty claims of the base paper.

## Base-paper scope

- exactly two voltage--recovery modules and two fixed scaled delay atoms;
- source-history feedback of size \(O(\varepsilon)\), with physical delays
  \(\tau_k=\theta_k/\sqrt\varepsilon\);
- one fixed, non-actuated transverse recovery coupling that removes the extra
  recovery center while vanishing on the critical recovery line;
- fixed local entry, exit, matching, and phase conditions;
- a geometric intersection of selected local slow histories, not a global
  spike detector;
- delayed van der Pol only as the published scalar calibration.

General finite \(N\), moving delay support, arbitrary node heterogeneity,
three-coordinate control, graphon limits, strong delays, and global pulse
events are promotion targets or later work, not claims of the base paper.

## Target: one theorem

For the fixed two-delay redistribution parameter \(\eta\), prove that the
selected RFDE canard parameter satisfies

\[
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =c_\perp K\eta(\theta_0-\theta_1)\delta^3
 +O(\delta^4|\eta|+\delta^3\eta^2),
 \qquad \delta=\sqrt\varepsilon,
\]

even though the total delayed gain and critical projected delay measure are
independent of \(\eta\). The actual coefficient, history lift, and uniform
remainder must be proved for the final RFDE. The current value
\(c_\perp=1/(4\alpha)\) is a formal candidate, not a result.

The precise claim hierarchy and falsification gates are in
[docs/flagship-research-design.md](docs/flagship-research-design.md). The
general-network specifications in
[docs/scope-and-theorems.md](docs/scope-and-theorems.md) are promotion
contracts, not proved inputs to this theorem.

## First feasibility result

The reference-template audit has produced four substantive corrections:

1. after phase fixing, a valid one-gap Lin formulation must have Fredholm
   index \(-1\), zero kernel, and one-dimensional cokernel; adjoining the
   scalar Lin jump then gives an invertible index-zero operator. Verifying
   these properties for the frozen RFDE model remains a proof gate;
2. two identical modules coupled only through \(O(\varepsilon)\) delayed
   diffusion inherit a repeated node-canard degeneracy at \(\varepsilon=0\).
   In the canonical symmetric inner problem the first relative splitting
   projection cancels and the formal second coefficient is nonzero, predicting
   a potentially severe \(G_\perp=O(\varepsilon^{-1})\) conditioning.
3. an exact two-delay family can keep both the total gain matrix and projected
   \(M_1^{(2)}\) fixed while changing transverse forcing and admitting a
   nonzero local nonlinear return channel. Hence the scalar moment does not
   determine the full range equation; a general law must calculate the
   transverse resolvent functional or prove its dynamic cancellation;
4. voltage synchronization alone leaves \(N-1\) transverse recovery centers
   and an \(N+1\)-dimensional generalized center. The proof reference now
   adds fixed \(E(P-I)w\), producing one collective length-two Jordan chain
   and hyperbolic transverse current-state blocks. Even then, each transverse
   RFDE Lin block still needs a history-space Fredholm trace pair. The
   reduced current-state skeleton has the necessary diagnostic
   \(d_-+d_+=2\); pinning both endpoints fails that diagnostic but is not, by
   itself, an RFDE index calculation.

Thus the weak-only and voltage-only classes are negative controls. The RFDE
Fredholm upper bound and uniform threshold remainder remain open; neither the
finite-dimensional spectrum nor a hard-endpoint matrix is presented as their
proof.

## Repository map

- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/flagship-research-design.md` -- proof-first main theorem, shortest dependency chain, stop/go gates, and paper architecture;
- `docs/scope-and-theorems.md` -- model, Lin-gap definition, main theorem specification, and stop/go gates;
- `docs/lin-gap-feasibility.md` -- \(\mathbb R^4\) reference full-history BVP template and correct Fredholm index bookkeeping;
- `docs/full-network-lin-operator.md` -- dual-scaffold \(2N\)-state operator contract, transverse trace-index audit, modal theorem target, and voltage-only negative control;
- `docs/two-module-reference.md` -- frozen FHN benchmark and weak-only transverse obstruction;
- `docs/two-module-moment-counterexample.md` -- exact mode-closure lemma, fixed-moment range-forcing counterexample, and Perron no-go result;
- `docs/shared-recovery-moment.md` -- repaired one-slow-variable benchmark and formal nonzero transverse dynamic-adjoint coefficient, with endpoint terms exposed;
- `docs/derivation-leading-moment.md` -- formally checked scalar/common-row-measure coefficients and the missing remainder obligations;
- `docs/sprint-01.md` -- first two-week execution plan linked to GitHub issues;
- `manuscript/outline.md` -- single-paper narrative, figures, and evidence standard;
- `references/references.bib` -- curated and deduplicated primary references;
- `src/canard_control/transverse_modes.py` -- executable weak-only inner splitting audit;
- `src/canard_control/reference_fhn.py` -- exact collective algebra for the dual-scaffold two-module benchmark;
- `src/canard_control/full_network_blocks.py` -- exact finite-\(N\) collective/transverse projectors, layer residuals, and dual-scaffold singular-Jacobian audit;
- `src/canard_control/two_module_moment.py` -- exact two-layer moment/range-forcing counterexample;
- `src/canard_control/shared_recovery_moment.py` -- executable shared-recovery inner and finite-section adjoint calculations;
- `experiments/transverse_lin_sweep.py` -- finite-interval boundary-condition diagnostic, explicitly not an RFDE inverse certificate;
- `tests/` -- symbolic and numerical regression tests.

## Project tracking

- [Flagship-paper epic](https://github.com/h-lu/canard-aware-network-control/issues/9)
- [Milestone: Flagship paper v1](https://github.com/h-lu/canard-aware-network-control/milestone/1)

## Immediate decision gate

Before large simulations, the project must write the single final two-module
RFDE, rerun its exact algebra, prove the relevant RFDE spectral gap, and
construct a parameter-regular two-dimensional invariant history manifold with
an injective history embedding. Only then may the formal transverse coefficient
be promoted to a geometric canard-root law. The full \(2N\)-state Lin
operator, an \(N\)-uniform inverse, and three-coordinate control are attempted
only after that base theorem passes its geometry and remainder gates.
