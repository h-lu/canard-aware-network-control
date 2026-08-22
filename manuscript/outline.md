# Flagship manuscript outline

Status: **base-paper outline under a model-selection gate, followed by a
conditional promotion outline.** The exact local algebra, relevant-root
count, and Lipschitz compact-tube graph are proved. The mixed jet is fixed by
the formal invariance recursion, while its graph remainder, the whole-line
coefficient, and the physical long-delay root remain proof obligations in
`docs/k1-tail-compatibility.md`. The alternative fixed-physical-delay route is
recorded in `docs/model-repair-options.md`.

## Proof-first base paper

Working title: **Transverse Delay Effects on a Canard Threshold in a
Two-Module FitzHugh--Nagumo System**

1. **Introduction and main theorem**
   - Same total delayed gain and same critical projected delay measure.
   - Nonzero transverse delay organization and the threshold law.
   - Zhang et al. (2026) supplies the scalar comparison case; no theorem is
     imported into the FHN system without verifying its hypotheses.
2. **The fixed two-module RFDE**
   - Final positive two-layer family and fixed recovery coupling.
   - Exact fold, projection, positivity, and singular-spectrum identities.
3. **The nonlocal invariant manifold**
   - Proved Lipschitz history graph and injective complete-history map; no
     backward RFDE initial-value problem is used.
   - Open finite-order mixed-regularity lemma and Taylor remainder.
4. **The reduced fold jet**
   - Stable transverse delay response.
   - Symbolically determined mixed vector-field jet and the conditional
     whole-line candidate \(c_\perp=1/(4\alpha)\).
5. **The canard intersection**
   - Long-delay option: selected-trace, growing-tube, and logarithmic matching
     estimates.
   - Fixed-delay option: regular \(K_1\) third-order splitting with an
     \(O(\delta^4)\) transverse effect.
   - Simple matching root and uniform remainder only after the selected option
     is complete.
   - Lift from the reduced intersection to complete RFDE histories.
6. **Numerical asymptotic check**
   - Normalized threshold difference with tolerance and maximum-step
     refinements.
7. **Discussion and promotion gates**
   - General finite-\(N\) root transfer only if its model-specific inverse is
     proved.
   - Three-coordinate control only if a certified rank bound requires no
     independent theory chain.

The base paper uses two figures: a transverse-return mechanism schematic and
a computed normalized threshold-limit plot.

---

## Promotion outline

Working title: **Canard-Threshold Transfer under Weak Delayed Feedback in Slow--Fast Networks**

## One-sentence target

For a finite weakly delayed slow--fast network near a controlled equitable reference class, formulate the canard as a one-dimensional RFDE Lin-matching root and derive its first-order response and second-order remainder under network, delay-measure, and node perturbations.

## Claim hierarchy

Everything in this hierarchy is a planned claim unless a supporting note
explicitly labels a finite-dimensional identity as proved.

1. **Theorem A -- RFDE Lin-gap transfer.** The geometric matching root is differentiable in the structural residual, with a first-variation formula and an explicit remainder depending on the transverse Green/Fredholm inverse bound.
2. **Proposition B -- first weighted delay moment and transverse correction.** The common-row-measure van der Pol class calibrates the parallel coefficient. Layerwise mode closure removes delayed-source transverse forcing, while full current/nonlinear/endpoint block closure is needed to eliminate the complete transverse functional. A fixed-total/fixed-moment range-forcing counterexample and a Perron no-go lemma show why that functional must be calculated, or its dynamic cancellation proved, outside the closure class.
3. **Corollary C -- concrete FHN control.** For one fixed two-module delayed FitzHugh--Nagumo system and the frozen linear, cubic, and delay-deformation actuators, prove a singular-value lower bound for the response map \((F,R_h,S_c)\) on a nonempty admissible region.
4. **Verification D.** Independent RFDE computations resolve the physical delay term, the network-transfer term, and the numerical error separately.

Exact equitable closure is a supporting lemma. The inverse-function theorem and scalar root perturbation step are tools, not novelty claims.

## Paper narrative

1. **Introduction and boundary with prior work**
   - Classical canard geometry supplies the fold and matching framework.
   - Delayed van der Pol work supplies the single-delay calibration.
   - Spectral network reduction supplies reference observables but not a nonhyperbolic root bound.
   - Frequency--amplitude control supplies two output coordinates but not a proved canard-safety coordinate.
   - If the promotion gates pass, state Theorem A as the promoted paper's sole
     flagship contribution.

2. **Reference RFDE and exact closure**
   - Weak-feedback/scaled-delay model and the fixed blown-up history interval.
   - Fixed instantaneous voltage--recovery synchronization scaffolds for the concrete FHN benchmark; both vanish on the collective history.
   - Exact singular-Jacobian comparison: weak-only and voltage-only negative controls versus the two-dimensional collective center of the dual-scaffold reference.
   - Common-row-measure synchronous RFDE and the two-module FHN reference class.
   - Residual norm for weights, delay measures, and node heterogeneity.
   - Why adjacency spectral gap alone does not control the fold passage.

3. **One-dimensional Lin matching problem**
   - \(\mathbb R^4\) reference-gap template versus the full \(2N\)-state operator for synchrony-breaking residuals.
   - Entry and exit data, matching section, phase condition, and complete \(2N\)-state history jump.
   - Full-history jump and the invariant-history construction of the backward-extendible repelling piece.
   - Trace-index audit: prove a history-space transverse Fredholm pair of index zero; \(d_-+d_+=2\) is only its reduced-skeleton diagnostic, and hard synchronization at both endpoints is excluded.
   - Zero-fiber implication: a zero complete-history jump must force the endpoint fiber coordinates to vanish before the root is called a slow-manifold intersection.
   - Post-phase Fredholm index \(-1\), one-dimensional cokernel, and the index-zero scalar-jump augmentation.
   - Transverse inverse \(G_\perp(\delta)\), \(\delta=\sqrt\varepsilon\).
   - Definition of the geometric Lin gap and its simple root.
   - Separate definition of experimental output-event thresholds.

4. **Proposition B: delayed van der Pol first-moment law**
   - Nonlocal invariant-history calculation.
   - Dirac-delay recovery as a published calibration, not a new result.
   - Common-row-measure closure and \((K/8)m_1\) calibration.
   - Two-module critical modes, \(M_1^{(2)}\), and the layerwise mode-closure condition.
   - Exact fixed-total/fixed-moment family with nonzero transverse forcing and nonlinear return.
   - Shared-recovery repair and its formal local coefficient \(\mathcal J_{\perp,0}=\eta(\theta_0-\theta_1)/4\), with the RFDE endpoint term kept explicit.
   - Perron no-go: positive-mode closure in nonnegative receiver-self diffusion collapses to common-row measures.
   - Dynamic-adjoint formula and singular-limit scaling for \(\mathcal J_{\perp,\delta}\), followed by a uniform \(O(\varepsilon^2)\) remainder in the admitted regime.

5. **Theorem A: structural transfer to the finite network**
   - Differentiability of the RFDE Lin problem in the chosen residual norm.
   - Lyapunov--Schmidt/range equation controlled by \(G_\perp(\delta)\).
   - First-variation functional and quadratic remainder.
   - Root transfer through the explicit transversality denominator.
   - Joint limit needed to distinguish an \(O(\varepsilon^{3/2})\) physical effect.

6. **Corollary C: two-module FHN three-coordinate control**
   - Fix the dual-scaffold equations, asymmetric output, parameter box, periodic branch, and the linear, cubic, and common-delay-shift actuators.
   - Periodic-orbit sensitivities for frequency and squared peak-to-peak amplitude.
   - Lin-root sensitivity for the positive safety margin \(S_c=a_{\rm op}-a_c\).
   - Factor the Jacobian through its \((F,R_h)\) block and safety Schur complement.
   - Prove a singular-value lower bound and a quantitative local inverse radius.
   - Give a structural one-/two-actuator obstruction; a rank-zero at one point is not called a no-go result.

7. **Verification D**
   - Independent Lin-BVP/continuation implementations.
   - Root enclosure from a gap residual divided by a derivative lower bound.
   - Separate physical delay, full/reduced transfer, and numerical discretization errors.
   - Held-out network residuals and negative controls.

8. **Discussion**
   - What is proved, computationally enclosed, or only suggested.
   - Failure modes: multiple Lin gaps, rapidly growing \(G_\perp\), matrix-valued delay effects, peak switching, and actuator rank loss.
   - General rank-\(r\), graphons, strong delay, and nonnormal sparse networks remain future work.
   - Weak-only identical modules form a singular multi-canard limit: the canonical inner first splitting cancels and the formal second coefficient predicts \(G_\perp=O(\varepsilon^{-1})\).

## Planned figures

1. RFDE Lin matching: all transverse coordinates matched and one adjoint gap retained.
2. Exact reference network, common row-delay measure, and controlled residual.
3. First-moment coefficient with a uniform-remainder test.
4. Full/reduced root displacement versus the predicted first variation.
5. Two-module FHN singular-value region and controlled trajectories at matched frequency/amplitude but different safety margins.

## Required negative controls

- perturb the network along residual directions annihilated and not annihilated by the first-variation functional;
- shuffle delays while preserving their unweighted histogram;
- preserve \(m_1\) while changing higher moments;
- include a trajectory-close but threshold-wrong reduction;
- compare one-, two-, and three-actuator families;
- repeat every root calculation with two independent RFDE discretization/continuation routes.

## Submission rule

If Gates E and F pass and the promoted paper is adopted, its abstract leads
with Theorem A. Proposition B, Corollary C, and Verification D are subordinate
parts of the same proof chain. No scalar \(K\Theta/8\), generic
inverse-function theorem, ordinary equitable closure, or earlier RK
chain-tree result is presented as a new contribution.
