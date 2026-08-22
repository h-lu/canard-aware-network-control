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
- fixed outer Fenichel selections, matching section, and phase convention;
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
independent of \(\eta\). The Lipschitz compact-tube history graph is proved;
the local mixed vector-field jet is uniquely determined by the formal
invariance recursion and checked symbolically. The candidate root coefficient
\(c_\perp=1/(4\alpha)\) still depends on a
whole-line pairing and is conditional on the selected-tail and growing-tube
estimates listed below.

The precise claim hierarchy and falsification gates are in
[docs/flagship-research-design.md](docs/flagship-research-design.md). The
general-network specifications in
[docs/scope-and-theorems.md](docs/scope-and-theorems.md) are promotion
contracts, not proved inputs to this theorem.

## Current proof status

The base project now has exact algebra, a proved Lipschitz local graph, and
two sharply identified analytic gaps.

1. **Exact model and spectrum.** The final two-module equation, anisotropic
   blow-up, delay-layer identities, fold data, and singular Jordan structure
   are exact. A separate Rouché--Schur argument proves that the scaled RFDE
   has exactly two simple relevant characteristic roots, near \(\pm i\), and a
   uniform complementary characteristic-root gap.
2. **Compact-tube history reduction.** A constructive contraction proves a
   unique bounded Lipschitz special-flow history graph and an injective
   complete-history map on a fixed compact fold tube. This avoids treating
   backward RFDE evolution as an initial-value problem. The finite-order
   mixed-jet upgrade is specified but not yet publication-complete.
3. **Formal local jet and conditional coefficient.** The invariance recursion
   and exact symbolic division give
   \[
   \partial_\eta q_{2,X}(\gamma_0(s))
   =-\frac{K(\theta_0-\theta_1)}{4\alpha}s.
   \]
   If the selected-tail estimates justify the whole-line Gaussian pairing,
   the parameterized second-order splitting gives
   \[
   c_\perp=\frac{1}{4\alpha},\qquad
   \mu_c(\delta,\eta)-\mu_c(\delta,0)
   =\frac{K\eta(\theta_0-\theta_1)}{4\alpha}\delta^3
   +O(\delta^4|\eta|+\delta^3\eta^2).
   \]
   The displayed root coefficient is therefore conditional, not a theorem on
   a fixed compact tube.
   Promoting this formal jet to a remainder-controlled graph coefficient
   first requires closing the mixed-jet fiber lemma.
4. **Remaining long-delay gate.** Individual long-delay backtrack maps have no
   uniform fixed-neighborhood \(C^1\) bound, so the standard \(K_1\) route is
   not yet applicable when \(\tau_k=\theta_k/\delta\). A logarithmic matching
   argument can suppress the resulting endpoint growth, but three
   estimates remain open: a one-sided selected-trace tame bound, a
   growing-tube graph remainder, and normalized gap-derivative bounds. Until
   they are proved, the displayed root law is conditional rather than the
   completed RFDE theorem.
5. **Numerical diagnostic.** Literal method-of-steps integration of the exact
   four-dimensional chart gives
   \([\nu_c(\delta,h)-\nu_c(\delta,-h)]/(2\delta h)\) converging from
   \(-0.1969771\) to \(-0.2036174\), against the predicted
   \(K(\theta_0-\theta_1)/(4\alpha)=-0.2041241\). This is strong
   falsification evidence, not a replacement for the missing tail estimates.

## Repository map

- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/flagship-research-design.md` -- proof-first main theorem, shortest dependency chain, stop/go gates, and paper architecture;
- `docs/scope-and-theorems.md` -- general-network promotion contract and its stop/go gates;
- `docs/lin-gap-feasibility.md` -- \(\mathbb R^4\) reference full-history BVP template and correct Fredholm index bookkeeping;
- `docs/full-network-lin-operator.md` -- dual-scaffold \(2N\)-state operator contract, transverse trace-index audit, modal theorem target, and voltage-only negative control;
- `docs/two-module-reference.md` -- frozen FHN benchmark and weak-only transverse obstruction;
- `docs/two-module-moment-counterexample.md` -- exact mode-closure lemma, fixed-moment range-forcing counterexample, and Perron no-go result;
- `docs/shared-recovery-moment.md` -- repaired one-slow-variable benchmark and formal nonzero transverse dynamic-adjoint coefficient, with endpoint terms exposed;
- `docs/derivation-leading-moment.md` -- formally checked scalar/common-row-measure coefficients and the missing remainder obligations;
- `docs/final-model-exact-algebra.md` -- exact final-model algebra and singular Jordan structure;
- `docs/final-model-blowup.md` -- exact anisotropic fold chart and projected/full-vector residual checks;
- `docs/rfde-relevant-spectrum.md` -- Rouché--Schur count of the two relevant RFDE roots and complementary gap;
- `docs/special-flow-graph-theorem.md` -- proved Lipschitz compact-tube history graph and the open finite-jet upgrade;
- `docs/reduced-canard-root.md` -- conditional second-order splitting template and exact symbolic integrands;
- `docs/k1-tail-compatibility.md` -- long-delay \(K_1\) obstruction, logarithmic rescue lemma, and the three open estimates;
- `docs/model-repair-options.md` -- comparison of the long-delay theorem with a lower-risk fixed-physical-delay variant;
- `docs/sprint-01.md` -- first two-week execution plan linked to GitHub issues;
- `manuscript/outline.md` -- single-paper narrative, figures, and evidence standard;
- `references/references.bib` -- curated and deduplicated primary references;
- `src/canard_control/transverse_modes.py` -- executable weak-only inner splitting audit;
- `src/canard_control/reference_fhn.py` -- exact collective algebra for the dual-scaffold two-module benchmark;
- `src/canard_control/full_network_blocks.py` -- exact finite-\(N\) collective/transverse projectors, layer residuals, and dual-scaffold singular-Jacobian audit;
- `src/canard_control/two_module_moment.py` -- exact two-layer moment/range-forcing counterexample;
- `src/canard_control/shared_recovery_moment.py` -- executable shared-recovery inner and finite-section adjoint calculations;
- `src/canard_control/final_two_module.py` -- exact final-model algebra and characteristic determinant;
- `src/canard_control/final_model_blowup.py` -- exact chart construction and scaling audit;
- `src/canard_control/nonlocal_graph_jet.py` -- symbolic invariant-graph and mixed-jet calculation;
- `src/canard_control/reduced_canard_root.py` -- conditional splitting and exact Gaussian-integral checks;
- `src/canard_control/exact_chart_threshold_diagnostic.py` -- literal method-of-steps integration and finite-section KS energy-gap root for the exact four-dimensional chart, explicitly diagnostic rather than a proof;
- `experiments/transverse_lin_sweep.py` -- finite-interval boundary-condition diagnostic, explicitly not an RFDE inverse certificate;
- `experiments/exact_chart_threshold_diagnostic.py` -- reproducible central-difference convergence table for the formal transverse threshold coefficient;
- `docs/exact-chart-threshold-diagnostic.md` -- archived numerical table and history/section-dependence disclaimer;
- `tests/` -- symbolic and numerical regression tests.

## Project tracking

- [Base-paper main theorem](https://github.com/h-lu/canard-aware-network-control/issues/10)
- [Flagship-paper epic](https://github.com/h-lu/canard-aware-network-control/issues/9)
- [Milestone: Flagship paper v1](https://github.com/h-lu/canard-aware-network-control/milestone/1)

## Model decision gate

The exact algebraic return channel has been identified formally, but the paper
must choose one of two honest theorem routes before further promotion work:

- keep the high-novelty long-delay scaling
  \(\tau_k=\theta_k/\delta\), retain the \(O(\delta^3)\) effect, and prove the
  three new logarithmic-tail estimates; or
- use fixed physical delays \(\tau_k=O(1)\), which restores the standard
  \(K_1\) geometry but moves the first transverse effect to
  \(O(\delta^4)\).

The full \(2N\)-state Lin transfer and three-coordinate control remain frozen
until one of these base theorems is complete.
