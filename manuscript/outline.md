# Flagship manuscript outline

Working title: **Canard-Threshold Transfer under Weak Delayed Feedback in Slow--Fast Networks**

## One-sentence target

For a finite weakly delayed slow--fast network near a controlled equitable reference class, formulate the canard as a one-dimensional RFDE Lin-matching root and derive its first-order response and second-order remainder under network, delay-measure, and node perturbations.

## Claim hierarchy

1. **Theorem A -- RFDE Lin-gap transfer.** The geometric matching root is differentiable in the structural residual, with a first-variation formula and an explicit remainder depending on the transverse Green/Fredholm inverse bound.
2. **Proposition B -- first weighted delay moment.** The common-row-measure van der Pol class calibrates the coefficient; for the exact two-module class, a mode-closure condition selects \(M_1^{(2)}\) and yields a uniform \(O(\varepsilon^2)\) remainder.
3. **Corollary C -- concrete FHN control.** For one fixed two-module delayed FitzHugh--Nagumo system and the frozen linear, cubic, and delay-deformation actuators, the response map \((F,R_h,S_c)\) has a proved singular-value lower bound on a nonempty admissible region.
4. **Verification D.** Independent RFDE computations resolve the physical delay term, the network-transfer term, and the numerical error separately.

Exact equitable closure is a supporting lemma. The inverse-function theorem and scalar root perturbation step are tools, not novelty claims.

## Paper narrative

1. **Introduction and boundary with prior work**
   - Classical canard geometry supplies the fold and matching framework.
   - Delayed van der Pol work supplies the single-delay calibration.
   - Spectral network reduction supplies reference observables but not a nonhyperbolic root bound.
   - Frequency--amplitude control supplies two output coordinates but not a proved canard-safety coordinate.
   - State Theorem A as the sole flagship contribution.

2. **Reference RFDE and exact closure**
   - Weak-feedback/scaled-delay model and the fixed blown-up history interval.
   - Fixed instantaneous transverse scaffold for the concrete FHN benchmark; it vanishes on the collective history.
   - Common-row-measure synchronous RFDE and the two-module FHN reference class.
   - Residual norm for weights, delay measures, and node heterogeneity.
   - Why adjacency spectral gap alone does not control the fold passage.

3. **One-dimensional Lin matching problem**
   - Entry and exit data, matching section, and phase condition.
   - Full-history jump and the center/solution-manifold construction of the backward-extendible repelling piece.
   - Post-phase Fredholm index \(-1\), one-dimensional cokernel, and the index-zero scalar-jump augmentation.
   - Transverse inverse \(G_\perp(\delta)\), \(\delta=\sqrt\varepsilon\).
   - Definition of the geometric Lin gap and its simple root.
   - Separate definition of experimental output-event thresholds.

4. **Proposition B: delayed van der Pol first-moment law**
   - Nonlocal center-manifold/history calculation.
   - Dirac-delay recovery as a published calibration, not a new result.
   - Common-row-measure closure and \((K/8)m_1\) calibration.
   - Two-module critical modes, \(M_1^{(2)}\), and the leading mode-closure condition.
   - Uniform \(O(\varepsilon^2)\) remainder and the possible same-order transverse resolvent term.

5. **Theorem A: structural transfer to the finite network**
   - Differentiability of the RFDE Lin problem in the chosen residual norm.
   - Lyapunov--Schmidt/range equation controlled by \(G_\perp(\delta)\).
   - First-variation functional and quadratic remainder.
   - Root transfer through the explicit transversality denominator.
   - Joint limit needed to distinguish an \(O(\varepsilon^{3/2})\) physical effect.

6. **Corollary C: two-module FHN three-coordinate control**
   - Fix the scaffolded equations, asymmetric output, parameter box, periodic branch, and the linear, cubic, and common-delay-shift actuators.
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

The abstract leads with Theorem A. Proposition B, Corollary C, and Verification D are subordinate parts of the same proof chain. No scalar \(K\Theta/8\), generic inverse-function theorem, ordinary equitable closure, or earlier RK chain-tree result is presented as a new contribution.
