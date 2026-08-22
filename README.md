# Canard-threshold transfer under weak delayed feedback

Research repository for one flagship paper:

> **Canard-threshold transfer under weak delayed feedback in slow--fast networks, with a concrete frequency--amplitude--safety corollary**

## Central question

When a biological network with weak delayed feedback is close to a canard explosion, can a reduced RFDE predict the **manifold-matching threshold** of the full finite network with a controlled error?

The first paper has one mathematical spine:

1. formulate the delayed canard as a one-dimensional Lin matching gap;
2. prove the gap and its simple root respond differentiably to finite-network residuals;
3. calculate the leading topology-weighted delay functional in a controlled model class.

A two-module delayed FitzHugh--Nagumo control target and planned residual-based
computation support this theorem program. They are not parallel novelty
claims.

## Frozen first-paper scope

- finite networks near an exact equitable two-module skeleton whose one-gap Fredholm hypothesis is verified rather than inferred from equitability;
- weak delayed feedback \(J=O(\varepsilon)\) and scaled delays \(\tau_{ij}=\Theta_{ij}/\sqrt{\varepsilon}\), with \(\Theta_{ij}\) in a compact set;
- fixed instantaneous voltage and recovery synchronization scaffolds in the concrete FHN control benchmark; both vanish on the collective history and neither is an actuator;
- a fixed entry/exit formulation, phase condition, and one-dimensional Lin gap after all transverse matching conditions are imposed;
- a compatible strong history space or delay-measure norm in which delay translations are controlled;
- an explicit transverse RFDE Green/Fredholm inverse bound \(G_\perp(\sqrt\varepsilon)\), rather than adjacency spectral gap alone;
- delayed van der Pol as the analytic calibration model;
- a two-module delayed FitzHugh--Nagumo network as the biological benchmark;
- three design coordinates: linear feedback gain, nonlinear feedback gain, and a realizable weighted delay moment.

General rank-\(r\) closure, graphon limits, arbitrary sparse nonnormal networks, strong delays, and nonsmooth all-node thresholds are extensions, not claims of the first paper.

## Targets: one theorem, one proposition, one corollary

1. **Main theorem -- RFDE Lin-gap threshold transfer.** Near an exact reference network, the full-network canard matching root has a first-order structural response and a controlled second-order remainder. The constants expose \(G_\perp(\sqrt\varepsilon)\), root transversality, and the chosen residual norm.
2. **Explicit proposition -- first delay moment plus transverse correction.** Use the common-row-measure delayed van der Pol class as calibration, prove the two-module parallel \(M_1^{(2)}\) coefficient under layerwise mode closure, and otherwise retain an explicit transverse resolvent functional, with a uniform remainder.
3. **Concrete corollary -- two-module FHN control.** For three specified admissible actuators, derive the response matrix for frequency, squared amplitude, and canard safety margin and prove a nonzero singular-value lower bound on a declared parameter region.
4. **Validation module.** Enclose the Lin-gap root error by residual and refinement bounds; reuse the earlier ODE/RK threshold result only as a cited baseline.

These are research targets, not established results. The scalar and common-row-measure coefficients currently have formal polynomial-solvability checks, but not the uniform remainder required by the proposition. Precise statements and falsification gates are in [docs/scope-and-theorems.md](docs/scope-and-theorems.md).

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

Before large simulations, the project must construct the dual-scaffold full
\(2N\)-state Lin operator and complementary dichotomy/fiber endpoint bundles
(or an equivalent two-dimensional center-manifold lift), prove that every
transverse block has index zero and is an isomorphism, prove that the
collective augmentation has one cokernel direction, and obtain a usable
transverse inverse bound \(G_\perp(\sqrt\varepsilon)\). The operator contracts
and finite-dimensional algebra are fixed; their invariant-manifold and
Fredholm hypotheses are not. The first-delay coefficient and root
transversality are then checked inside the full formulation. Failure narrows
the theorem to the exact invariant class before any expensive computation.
