# Long-delay shifts of local canard connections

Research repository for the JNS manuscript:

> **Long-Delay Shifts of Local Canard Connections in Retarded Fast--Slow
> Systems**

The complete LaTeX manuscript, figures, appendices, cover letter, and
submission checklist are in [manuscript/jns](manuscript/jns).  The supporting
research design is [docs/flagship-research-design.md](docs/flagship-research-design.md).
General finite-network transfer and three-coordinate control are an active
successor program, but remain outside and are not claims of this paper.

Build and verify from the repository root with

```sh
python3 -m pip install -e '.[paper,test]'
make -C manuscript/jns paper
python3 -m pytest -q
```

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

The broader finite-network transfer and frequency--amplitude--safety control
programs remain separate successors in the repository. They are not
assumptions, promotions, or parallel novelty claims of the base paper.

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
 \mu_{c,\mathcal P}(\delta,\eta)-\mu_{c,\mathcal P}(\delta,0)
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
outer Fenichel maximal canard. Backward completeness alone does not select
one. Such a physical selection inherits the same coefficient only under the
separate, parameter-coherent compatible-selection and full-history
boundary-jet hypotheses in
[docs/canonical-long-delay-theorem.md](docs/canonical-long-delay-theorem.md)
and
[docs/paper-iii-outer-selection-blocker-and-repair.md](docs/paper-iii-outer-selection-blocker-and-repair.md).

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
   \(C_u^3C_\delta^3C_\nu^1C_\eta^2\) rectangular mixed regularity and an
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
5. **Physical outer-selection Gate D (repaired target open).** The original
   rule is now disproved as sufficient: bounded backward completeness does
   not select the repelling unstable coordinate, and exponential closeness
   does not control rectangular \(C_\nu^1C_\eta^2\) history jets. Transfer
   requires the open compatible-selection Gate P3-A\(^*\), with declared
   curve-wise Lyapunov--Perron boundary coordinates and exact common-graph
   normalization. The unforced causal alternative has an exact
   one-maximal-delay released history and a proved nonempty pulse/quiet
   transition set. Its unforced separator is still open, but the old local
   shortcut is now known to be insufficient: even an exact saddle separator
   need not classify all offsets by fixed-layer first hits when recovery
   drifts. The repaired route splits into an outer stable-foliation gate
   U-SF, a repaired moving-tube/lower-fold event gate U-EX, and the separate
   U-CAP biological capture/no-return gate. An exact Airy model shows that the
   lower-fold event root can be exponentially displaced from the geometric
   root; the physical comparison requires the stated fold-map factorization,
   and neither root is identified with the canard root without an additional
   theorem. A
   modified protocol that clamps only the collective recovery coordinate now
   has, for every sufficiently small fixed positive \(\delta\), a proved
   codimension-one complete-history pulse/quiet separator. This is an
   operational controlled threshold, not the unforced canard root.
6. **General-network successor theorem.** For arbitrary finite Markov
   networks with a common Dobrushin gap, one shared recovery resource, and
   heterogeneous fold curvature, a dimension-uniform history graph and
   canonical selected root are proved without a nontrivial synchrony
   quotient. Projection-neutral delay redistribution has the explicit
   resolvent coefficient
   \[
   -\frac{K}{2\alpha^2}\,
   \pi_N^T\operatorname{diag}(c_N)A_N^{-1}
   P_{\perp,N}\dot M_{1,N}\mathbf1,
   \]
   and an all-\(N\) family realizes a common nonzero value. The exact root
   remains preparation-indexed; physical outer selection is not inferred.
7. **Pulse-control successor theorems.** A size-uniform Halanay estimate
   separates transverse synchronization from output conditioning. Under the
   declared physical-root and one-coordinate canard-layer hypotheses, the
   original frequency--amplitude--safety response has an exponentially bad
   right-inverse lower bound. A reset-only operational actuator instead gives
   an exact block-triangular response and a quantitative inverse whenever the
   two-by-two frequency--amplitude block is certified. The corresponding FHN
   periodic package now supplies a reproducible Fourier-collocation orbit,
   derivative matrix, unique-extrema diagnostics, and a positive nine-sample
   floating response-box candidate. The directed periodic-orbit and response
   interval certificate remains open.
8. **Numerical diagnostic.** Literal method-of-steps integration of one
   finite-section exact-chart diagnostic gives
   \([\nu_c(\delta,h)-\nu_c(\delta,-h)]/(2\delta h)\) converging from
   \(-0.1969771\) to \(-0.2036174\), against the predicted
   \(K(\theta_0-\theta_1)/(4\alpha)=-0.2041241\). This is falsification
   evidence for the coefficient, not a proof that the diagnostic root equals
   the canonical history root or a physical outer root.

## Repository map

- `manuscript/jns/main.tex` -- JNS manuscript entry point;
- `manuscript/jns/sections/` and `manuscript/jns/appendices/` -- self-contained
  theorem, proof, numerical diagnostic, and technical estimates;
- `manuscript/jns/figures/` -- deterministic vector-figure sources and PDFs;
- `manuscript/jns/submission/` -- cover letter, editor suggestions, checklist,
  and claim-boundary report;
- `docs/literature-map.md` -- primary-literature boundary and novelty audit;
- `docs/flagship-research-design.md` -- proof-first main theorem, shortest dependency chain, stop/go gates, and paper architecture;
- [docs/general-network-canard-pulse-control-program.md](docs/general-network-canard-pulse-control-program.md) -- active successor program: arbitrary finite-\(N\) one-fold history graphs, vector-gap extension, physical pulse onset, and quantitative three-output control/no-go gates;
- [docs/dimension-uniform-special-flow-history-graph.md](docs/dimension-uniform-special-flow-history-graph.md) -- abstract dimension-uniform special-flow graph theorem with operator-TV delays, mixed jets, logarithmic fold tubes, and exact mild history embedding; network model fitting remains separate;
- [docs/banach-scale-history-schur-link.md](docs/banach-scale-history-schur-link.md) -- three-level \(C_b^9\to C_b^8\to C_b^7\) graph-response theorem, complete-history extension/restriction, levelwise Schur formulas, and conditional trace/endpoint transfer without a false same-space \(C^2\) implicit-function theorem;
- [docs/paper-ii-lifted-two-module-class.md](docs/paper-ii-lifted-two-module-class.md) -- exact arbitrary-size unequal-module lift, maximum-norm Gate A model-fitting audit (with weighted algebra retained only as a diagnostic), dimension-independent singular semigroup bound, and operator-TV non-equitable perturbation family;
- [docs/paper-ii-arbitrary-n-blowup-model-fit.md](docs/paper-ii-arbitrary-n-blowup-model-fit.md) -- exact arbitrary-\(N\) anisotropic blow-up, full stable-fiber shift, true divisibility checks, and dimension-uniform prepared-data fit to the abstract history-graph theorem;
- [docs/paper-ii-selected-root-lift-and-symmetry-breaking.md](docs/paper-ii-selected-root-lift-and-symmetry-breaking.md) -- exact compatible-canonical selected-gap/root lift for arbitrary positive module sizes, uniform inherited root coefficient, Reynolds nullity of the pure within-module breaker, and a genuinely non-equitable nonzero combined tangent;
- [docs/paper-ii-heterogeneous-curvature-selected-root.md](docs/paper-ii-heterogeneous-curvature-selected-root.md) -- dimension-uniform, synchrony-quotient-free canonical selected-root theorem for arbitrary finite Dobrushin networks, with an explicit nonzero topology-resolvent coefficient and all-\(N\) witness;
- [docs/paper-ii-shared-resource-dobrushin-class.md](docs/paper-ii-shared-resource-dobrushin-class.md) -- a genuinely arbitrary-\(N\) one-slow-resource class with a uniform Dobrushin contraction; its prepared graph is conditional on the stated tame cutoff and its physical root response remains open;
- [docs/shared-resource-order-three-cancellation.md](docs/shared-resource-order-three-cancellation.md) -- exact projection-neutral interior cancellation through the first two physical root orders in the homogeneous shared-resource class; endpoint/root consequences remain conditional;
- [docs/general-network-schur-melnikov-proof.md](docs/general-network-schur-melnikov-proof.md) -- Gate C calculus: exact graph/gap Schur derivatives, a conditional projection-neutral cubic root theorem with explicit constants, codimension-one genericity once a nonzero witness is known, and the strict direct-sum audit;
- [docs/general-network-vector-gap-codimension.md](docs/general-network-vector-gap-codimension.md) -- abstract complete-history vector-gap theorem, codimension-\(q\) canard locus, quantitative root bounds, and the robust actuator-count obstruction \(m\ge q\); network-specific index and rank remain open;
- [docs/multiple-recovery-center-obstruction.md](docs/multiple-recovery-center-obstruction.md) -- exact \((N+1)\)-dimensional singular center and persistent \(N-1\) slow-root obstruction for standard independent recoveries; the full-history cokernel dimension remains open;
- [docs/paper-iii-physical-outer-pulse-bridge.md](docs/paper-iii-physical-outer-pulse-bridge.md) -- proved singular two-channel geometry, an explicit distinction among geometric, lower-fold-event, biological-channel, and amplitude roots, and the open or conditional outer-history, fold-map, U-CAP, and landing gates;
- [docs/paper-iii-outer-selection-blocker-and-repair.md](docs/paper-iii-outer-selection-blocker-and-repair.md) -- exact counterexample to backward-completeness as a selection rule, curve-restricted history equations, anchored flat-error estimate, repaired Gate P3-A\(^*\), and the causal reset alternative;
- [docs/paper-iii-causal-reset-separator.md](docs/paper-iii-causal-reset-separator.md) -- exact causal release history, voltage-memory overwrite and recovery non-erasure, fixed-fast-time pulse/quiet passage cylinders, and a proved nonempty reset-transition set; its former all-in-one R-S target is decomposed below;
- [docs/paper-iii-unforced-separator-stop-go.md](docs/paper-iii-unforced-separator-stop-go.md) -- exact ODE-subclass obstruction to deriving an unforced first-hit boundary from a local saddle separator and fixed-layer blocks, plus the former U-EX target repaired into a U-SF geometric root, moving-tube/lower-fold event root, and U-CAP biological boundary; it does not disprove the physical FHN separator;
- [docs/paper-iii-unforced-geometric-separator.md](docs/paper-iii-unforced-geometric-separator.md) -- Gate U-SF theorem package: exact middle-branch action obstruction, the narrow outer-tracker and dominated-history-trichotomy hypotheses, and the conditional unique selected geometric reset separator, explicitly without a pulse/quiet outcome claim;
- [docs/paper-iii-unforced-lower-fold-exchange.md](docs/paper-iii-unforced-lower-fold-exchange.md) -- Gate U-EX stop/go theorem: proved physical lower-fold orientation and reset-to-fold action, exact Airy all-offset sign obstruction, moving slow-base/fold event repair, and the still-open physical fold-map and separate U-CAP capture/no-return gates;
- [docs/paper-iii-collective-clamp-separator.md](docs/paper-iii-collective-clamp-separator.md) -- exact collective-recovery-clamped saddle, one-unstable-root criterion, fixed-\(\delta\) complete-history pulse/quiet separator, deadline deadband, and explicit separation from the open unforced U-SF/U-EX/U-CAP route;
- [docs/paper-iv-canard-conditioning-no-go.md](docs/paper-iv-canard-conditioning-no-go.md) -- exact row-cancellation bound showing when amplitude and pulse-safety coordinates become exponentially ill-conditioned inside a canard window; delayed-network applicability is conditional on Paper III;
- [docs/paper-iv-periodic-rfde-adjoints.md](docs/paper-iv-periodic-rfde-adjoints.md) -- proved period/frequency, peak-envelope, distributional amplitude, and causal event adjoints for discrete-delay RFDEs, with exact synchronous-FHN specialization and an explicitly conditional three-row response target;
- [docs/paper-iv-fhn-control-no-go.md](docs/paper-iv-fhn-control-no-go.md) -- full-network modal decomposition, size-uniform transverse Halanay theorem, and sharp two-scale inverse-conditioning no-go for the declared FHN outputs under explicit root/layer hypotheses;
- [docs/paper-iv-reset-only-block-control.md](docs/paper-iv-reset-only-block-control.md) -- controlled complete-history threshold IFT, exact reset-only block-triangular response, singular-value and target-radius bounds, Hopf frequency--amplitude witness, and the still-open validated FHN box;
- [docs/paper-iv-fhn-periodic-box-candidate.md](docs/paper-iv-fhn-periodic-box-candidate.md) -- executable synchronous two-delay FHN periodic BVP, moving-delay sensitivities, extrema/invertibility diagnostics, positive finite-sample response-box candidate, and the direct interval plus ODE-persistence proof contracts; it is explicitly not a validated interval certificate;
- `src/canard_control/fhn_periodic_candidate.py` -- odd-Fourier BVP/continuation, analytic period column, gain sensitivities, discrete-adjoint audit, sampled box, and ODE-persistence-route diagnostics;
- `experiments/fhn_periodic_box_candidate.py` with `experiments/requirements-fhn-periodic-candidate.txt` -- one-command candidate reproduction and exact NumPy/SciPy dependencies;
- `experiments/results/fhn_periodic_box_candidate.json` -- machine-readable binary64 result and software/arithmetic provenance, with all validated-interval flags set to false;
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
- `src/canard_control/lifted_two_module_network.py`, `src/canard_control/lifted_network_blowup.py`, and `src/canard_control/lifted_selected_root_response.py` -- exact arbitrary-size lifting, blow-up/model-fit, Reynolds, and non-equitable response audits;
- `src/canard_control/shared_resource_markov.py` -- Dobrushin contraction and one-shared-resource network identities;
- `src/canard_control/shared_resource_response.py` -- exact constant-history cancellation audit for projection-neutral shared-resource directions;
- `src/canard_control/heterogeneous_curvature_root.py` -- exact arbitrary-\(N\) curvature/resolvent root coefficient and normalized no-synchrony-quotient witness;
- `src/canard_control/block_schur_response.py` -- exact block-response and projection-neutral Schur regressions;
- `src/canard_control/physical_pulse_bridge.py` -- singular fast-channel, Sturm, section-orientation, and detector-action calculations;
- `src/canard_control/causal_reset_separator.py` -- exact causal reset, memory overwrite/non-erasure, endpoint-rank, and scalar root-transfer certificates;
- `src/canard_control/unforced_separator_obstruction.py` -- exact drifting-saddle exit-time and fixed-layer miss identities that falsify the local shortcut to an unforced first-hit separator;
- `src/canard_control/unforced_geometric_separator.py` -- singular reset-layer action and unstable-vector audit, logarithmic outer-error propagation, weighted Green/strong-unstable domination ledgers, and scalar geometric-separator root bound;
- `src/canard_control/unforced_lower_fold_exchange.py` -- exact rational lower-fold signs, physical middle-branch action, and underflow-safe Airy fold-boundary diagnostics;
- `src/canard_control/clamped_reset_separator.py` -- collective-clamp equilibrium, unstable-index, deadline, and large-delay spectral diagnostics;
- `src/canard_control/outer_selection_coherence.py` -- exact outer-selection nonuniqueness, mixed-jet blow-up, and anchored-boundary suppression diagnostics;
- `src/canard_control/canard_conditioning.py` -- response-row cancellation, determinant shear, and inverse-conditioning bounds;
- `src/canard_control/periodic_rfde_sensitivity.py` -- discrete retarded/advanced transpose, moving-delay, periodic-response, amplitude, and causal landing-adjoint regressions;
- `src/canard_control/fhn_control_no_go.py` -- exact transverse mode decomposition, Halanay constants, response no-go bounds, and sharpness diagnostics;
- `src/canard_control/operational_control_repair.py` -- reset-only block response, quantitative inverse radius, Hopf response, and floating interval-candidate diagnostics;
- `src/canard_control/multiple_recovery_center.py` -- exact fold-chain, recovery-center, slow-root, and conditional linear matching-count checks;
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
- [Paper II: general finite-network canard response](https://github.com/h-lu/canard-aware-network-control/milestone/2)
- [Paper III: physical canard to pulse onset](https://github.com/h-lu/canard-aware-network-control/milestone/3)
- [Paper IV: biological pulse-coordinate control](https://github.com/h-lu/canard-aware-network-control/milestone/4)
- [Paper II epic](https://github.com/h-lu/canard-aware-network-control/issues/4)
- [Paper III physical-selection epic](https://github.com/h-lu/canard-aware-network-control/issues/11)
- [Paper III pulse-event theorem](https://github.com/h-lu/canard-aware-network-control/issues/12)
- [Paper IV control/conditioning epic](https://github.com/h-lu/canard-aware-network-control/issues/5)

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

The general-network and pulse-control work has now been reopened as a
separate successor program. It remains outside this paper. Its primary
one-critical-mode proof route is a dimension-uniform invariant-history graph;
the full \(2N\)-state Lin--Fredholm route is retained for multiple center
directions and vector gaps.
