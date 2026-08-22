# Transverse delay organization and a canonical history-canard root

Research repository for one proof-first flagship paper:

> **Transverse Delay Organization and a Canonical Local History-Canard Root
> in a Two-Module FitzHugh--Nagumo RFDE**

The current proof-first submission design is
[docs/flagship-research-design.md](docs/flagship-research-design.md). It
freezes a two-module canonical local history-connection theorem as the
minimum publishable core. Its proof components and independent skeptical
audit are complete. General finite-network transfer and three-coordinate
control remain frozen and are not claims of this paper.

## Central question

Can two weakly delayed FitzHugh--Nagumo modules have the same total delayed
gain and the same delay measure seen by the critical projection, yet have
different canonical local history-connection roots because the delay forcing
passes through a stable transverse mode?

The first paper has one mathematical spine:

1. freeze one two-module, two-delay RFDE and prove its exact singular spectrum;
2. construct its two-dimensional invariant history graph, including the
   logarithmically growing tube needed for long physical delays;
3. construct phase-normal one-sided traces and prove that their simple gap
   root is equality of the two retained complete RFDE histories.

The broader finite-network Lin transfer and frequency--amplitude--safety
control programs remain in the repository as frozen future work. They are
not assumptions, promotions, or parallel novelty claims of the base paper.

## Base-paper scope

- exactly two voltage--recovery modules and two fixed scaled delay atoms;
- source-history feedback of size \(O(\varepsilon)\), with physical delays
  \(\tau_k=\theta_k/\sqrt\varepsilon\);
- one fixed, non-actuated transverse recovery coupling that removes the extra
  recovery center while vanishing on the critical recovery line;
- the canonical prepared-tail selection, matching section, and phase
  convention of the local theorem;
- an exact intersection of two retained local RFDE histories, not an
  assertion about every physical outer Fenichel family and not a global spike
  detector;
- delayed van der Pol only as the published scalar calibration.

General finite \(N\), moving delay support, arbitrary node heterogeneity,
three-coordinate control, graphon limits, strong delays, and global pulse
events are frozen or later work, not claims of the base paper.

## Proved canonical theorem

For the fixed two-delay redistribution parameter \(\eta\), the component
proofs assemble the canonical local root law

\[
 \mu_c(\delta,\eta)-\mu_c(\delta,0)
 =\frac{K(\theta_0-\theta_1)}{4\alpha}\,\delta^3\eta
 +O(\delta^4|\eta|+\delta^3\eta^2),
 \qquad \delta=\sqrt\varepsilon,
 \qquad \alpha=\frac{\sqrt6}{4}.
\]

even though the total delayed gain and critical projected delay measure are
independent of \(\eta\). The root is defined by the canonical prepared-tail
and phase convention, and zero gap is proved to be equality of the retained
complete histories under the injective history embedding. The growing-tube
graph, one-sided Green/phase trace proof, weighted contraction seam, and
independent falsification audit are complete. The exact finite-\(\delta\)
root is indexed by the fixed admissible preparation datum \(\mathcal P\),
while its displayed expansion is uniform over the declared bounded
preparation class.

This is not an unconditional theorem for an arbitrarily selected physical
outer Fenichel maximal canard. Such a physical selection inherits the same
coefficient only under the separate, parameter-coherent full-history
boundary-jet hypothesis in
[docs/canonical-long-delay-theorem.md](docs/canonical-long-delay-theorem.md).

The precise claim hierarchy and falsification gates are in
[docs/flagship-research-design.md](docs/flagship-research-design.md). The
general-network specifications in
[docs/scope-and-theorems.md](docs/scope-and-theorems.md) are frozen
future-work contracts, not proved inputs or active promotions of this theorem.

## Current proof status

The canonical route is proved; the physical outer-selection route remains
open.

1. **Exact model and spectrum.** The final two-module equation, anisotropic
   blow-up, delay-layer identities, fold data, and singular Jordan structure
   are exact. A separate Rouché--Schur argument proves that the scaled RFDE
   has exactly two simple relevant characteristic roots, near \(\pm i\), and a
   uniform complementary characteristic-root gap.
2. **Compact-tube history reduction.** A constructive contraction proves a
   unique bounded Lipschitz special-flow history graph and an injective
   complete-history map on a fixed compact fold tube. This avoids treating
   backward RFDE evolution as an initial-value problem. A triangular scale of
   common Banach fibers now proves the required
   \(C_u^3C_{\delta,\eta}^{3,2}\) mixed regularity and an
   \(O(\delta^3)\) fixed-tube graph remainder.
3. **Actual local graph jet.** The proved
   mixed regularity promotes the invariance recursion to a Taylor coefficient
   of the compact-tube graph, while exact symbolic division independently gives
   \[
   \partial_\eta q_{2,X}(\gamma_0(s))
   =-\frac{K(\theta_0-\theta_1)}{4\alpha}s.
   \]
4. **Canonical long-delay Gate D (passed).** A frozen
   target-dependent cutoff gives the required mixed jets and remainder on the
   logarithmically growing flow hull. Explicit one-sided Green operators remove
   the normally growing mode, fix the tangent phase, and construct the
   canonical attracting/repelling traces. The normalized gap calculation and
   injective history lift then give the exact coefficient and remainder above.
   The assembled theorem and verification record are in
   [docs/canonical-long-delay-theorem.md](docs/canonical-long-delay-theorem.md).
5. **Physical outer-selection Gate D (open).** No arbitrary outer Fenichel
   family is identified with the canonical traces. The extension is
   conditional on a fixed selection rule whose full-history boundary residual
   and rectangular \(C_\nu^1C_\eta^2\) jets have the stated tame bounds. The
   exact physical modal algebra is known; the parameter-coherent outer
   Lyapunov--Perron estimate is not.
6. **Numerical diagnostic.** Literal method-of-steps integration of one
   finite-section exact-chart diagnostic gives
   \([\nu_c(\delta,h)-\nu_c(\delta,-h)]/(2\delta h)\) converging from
   \(-0.1969771\) to \(-0.2036174\), against the predicted
   \(K(\theta_0-\theta_1)/(4\alpha)=-0.2041241\). This is falsification
   evidence for the coefficient, not a proof that the diagnostic root equals
   the canonical history root or a physical outer root.

## Repository map

- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/flagship-research-design.md` -- proof-first main theorem, shortest dependency chain, stop/go gates, and paper architecture;
- `docs/scope-and-theorems.md` -- frozen general-network future-work contract and its stop/go gates;
- `docs/lin-gap-feasibility.md` -- \(\mathbb R^4\) reference full-history BVP template and correct Fredholm index bookkeeping;
- `docs/full-network-lin-operator.md` -- dual-scaffold \(2N\)-state operator contract, transverse trace-index audit, modal theorem target, and voltage-only negative control;
- `docs/two-module-reference.md` -- frozen FHN benchmark and weak-only transverse obstruction;
- `docs/two-module-moment-counterexample.md` -- exact mode-closure lemma, fixed-moment range-forcing counterexample, and Perron no-go result;
- `docs/shared-recovery-moment.md` -- repaired one-slow-variable benchmark and formal nonzero transverse dynamic-adjoint coefficient, with endpoint terms exposed;
- `docs/derivation-leading-moment.md` -- formally checked scalar/common-row-measure coefficients and the missing remainder obligations;
- `docs/final-model-exact-algebra.md` -- exact final-model algebra and singular Jordan structure;
- `docs/final-model-blowup.md` -- exact anisotropic fold chart and projected/full-vector residual checks;
- `docs/rfde-relevant-spectrum.md` -- Rouché--Schur count of the two relevant RFDE roots and complementary gap;
- `docs/special-flow-graph-theorem.md` -- constructive Lipschitz compact-tube history graph and injective history map;
- `docs/mixed-jet-graph-proof.md` -- finite-scale mixed-jet closure and the uniform fixed-tube Taylor remainder;
- `docs/reduced-canard-root.md` -- conditional second-order splitting template and exact symbolic integrands;
- `docs/k1-tail-compatibility.md` -- long-delay \(K_1\) obstruction and logarithmic rescue mechanism;
- `docs/long-delay-selected-trace-proof.md` -- normalized trace-to-gap calculation and root displacement;
- [docs/growing-tube-graph-proof.md](docs/growing-tube-graph-proof.md) -- frozen-cutoff logarithmic-tube graph theorem and mixed remainder;
- [docs/green-phase-selected-traces.md](docs/green-phase-selected-traces.md) -- explicit one-sided Green operators, phase normalization, and canonical trace theorem;
- [docs/canonical-long-delay-theorem.md](docs/canonical-long-delay-theorem.md) -- dependency-explicit canonical history-connection theorem, exact root law, physical-selection corollary, and audit checklist;
- [docs/outer-modal-algebra.md](docs/outer-modal-algebra.md) -- exact physical modal equations and the still-open outer-selection boundary;
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
- [src/canard_control/green_phase.py](src/canard_control/green_phase.py) -- executable tangent/normal frame and one-sided Green identities;
- [src/canard_control/outer_modal_audit.py](src/canard_control/outer_modal_audit.py) -- exact physical modal equations, branch jets, and fast-gap audit;
- `src/canard_control/exact_chart_threshold_diagnostic.py` -- literal method-of-steps integration and finite-section KS energy-gap root for the exact four-dimensional chart, explicitly diagnostic rather than a proof;
- `experiments/transverse_lin_sweep.py` -- finite-interval boundary-condition diagnostic, explicitly not an RFDE inverse certificate;
- `experiments/exact_chart_threshold_diagnostic.py` -- reproducible central-difference convergence table for the formal transverse threshold coefficient;
- `docs/exact-chart-threshold-diagnostic.md` -- archived numerical table and history/section-dependence disclaimer;
- [tests/test_green_phase.py](tests/test_green_phase.py) -- exact tangent/normal frame and one-sided Green regression tests;
- [tests/test_outer_modal_audit.py](tests/test_outer_modal_audit.py) -- physical modal algebra, branch-jet, and fast-gap regression tests;
- `tests/` -- remaining symbolic and numerical regression tests.

## Project tracking

- [Base-paper main theorem](https://github.com/h-lu/canard-aware-network-control/issues/10)
- [Flagship-paper epic](https://github.com/h-lu/canard-aware-network-control/issues/9)
- [Milestone: Flagship paper v1](https://github.com/h-lu/canard-aware-network-control/milestone/1)

## Frozen theorem route

Route A was selected on 2026-08-22. The base paper retains the long-delay
scaling

\[
 \tau_k=\theta_k/\delta
\]

and proves an \(O(\delta^3)\) effect for the canonical local history root.
The canonical growing-graph, one-sided trace, gap, and history-lift components
of Gate D and the independent falsification audit have passed. The distinct
physical outer-selection
gate remains open and conditional on parameter-coherent full-history boundary
jets. The fixed-physical-delay variant remains only a documented fallback and
is not an active theorem target.

The full \(2N\)-state Lin transfer and three-coordinate control remain frozen
and outside this paper.
