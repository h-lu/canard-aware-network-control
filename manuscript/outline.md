# Flagship manuscript outline

Working title: **Observable-Projected Canard-Threshold Transfer and Frequency--Amplitude--Safety Control in Delayed Slow--Fast Networks**

## One-sentence claim

For weakly delayed slow--fast networks near an equitable low-rank skeleton, a specified aggregate canard threshold can be transferred from a reduced RFDE with controlled error and, under a verifiable rank condition, its safety margin can be assigned locally and independently of oscillation frequency and amplitude.

## Narrative

1. **Introduction**
   - Biological rhythms require frequency and amplitude control, but pulse onset adds a safety constraint near canard explosion.
   - Delayed canard asymptotics, network tipping reduction, and phase--amplitude control currently give separate pieces.
   - State the observable dependence and finite-network scope immediately.

2. **Network, observable, and threshold**
   - RFDE phase space and weak-delay scaling.
   - Exact equitable skeleton plus residual.
   - Common section and selected invariant manifolds.
   - Definition of the observable-projected threshold and safety margin.

3. **Exact delayed module reduction**
   - Invariant block-synchronous history space.
   - Delayed van der Pol calibration and two-module FitzHugh--Nagumo specialization.

4. **Canard splitting and delay-moment selection**
   - Blow-up chart and nonlocal center-manifold reduction.
   - Adjoint splitting functional.
   - First nonzero topology-weighted delay moment and remainder.

5. **Threshold transfer to the full network**
   - Splitting perturbation estimate.
   - Quantitative root shift.
   - Observable dependence and limits of transfer.

6. **Frequency--amplitude--safety control**
   - Periodic-orbit and splitting sensitivities.
   - Full-rank inverse-design theorem.
   - Rank-deficiency/no-go example.

7. **Certified computation**
   - Continuation/root pipeline.
   - RK or collocation error, history interpolation, reduction error, and interactions.
   - Fold-specific chain-tree diagnostic.

8. **Validation**
   - Delayed van der Pol coefficient recovery.
   - Exact and perturbed two-module FitzHugh--Nagumo networks.
   - Out-of-sample heterogeneous residuals and actuator targets.

9. **Discussion**
   - What is proved, what is numerically validated, and what is only suggested.
   - Extensions to distributed delays, graphons, and nonnormal sparse networks.

## Planned figures

1. Conceptual geometry: observable splitting, threshold, and three output coordinates.
2. Exact two-module reduction and residual decomposition.
3. Delay-moment selection: asymptotic prediction versus continuation.
4. Threshold-transfer error versus network residual, including uncertainty bars.
5. Singular-value map of the three-coordinate response Jacobian.
6. Controlled trajectories at matched frequency/amplitude but separated safety margins.

## Required negative controls

- change the observable while holding the network fixed;
- shuffle delays while preserving the unweighted delay histogram;
- preserve the leading weighted moment but alter higher moments;
- compare one-, two-, and three-actuator families;
- repeat every threshold plot under at least two discretization families.

## Submission rule

One paper only. Delay-moment selection and numerical certification are supporting sections of the flagship theorem chain, not separate manuscripts.
