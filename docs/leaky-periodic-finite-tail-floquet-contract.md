# Finite/tail and Floquet contract for the leaky periodic branches

Status: **the equation-level incompatibility and all changed majorants have
been independently audited; source-bound directed radii arguments now prove
both the inner and outer phase-fixed periodic RFDE orbits and their
phase-bordered inverses.  Neither Floquet index is promoted.**  This is the safe entry
point for [issue 20](https://github.com/h-lu/canard-aware-network-control/issues/20).

The implementation is
[leaky_periodic_validation.py](../src/canard_control/leaky_periodic_validation.py),
with structural and refusal tests in
[test_leaky_periodic_validation.py](../tests/test_leaky_periodic_validation.py).
The inner replay contract is implemented in
[leaky_periodic_branch_artifact.py](../src/canard_control/leaky_periodic_branch_artifact.py),
with its tracked body in
[autonomous_leaky_recovery_inner_branch_artifact.json](../experiments/results/autonomous_leaky_recovery_inner_branch_artifact.json)
and hostile replay tests in
[test_leaky_periodic_branch_artifact.py](../tests/test_leaky_periodic_branch_artifact.py).
The independently generated high-resolution outer replay is implemented in
[leaky_outer_high_resolution.py](../src/canard_control/leaky_outer_high_resolution.py),
with its tracked body in
[autonomous_leaky_recovery_outer_high_resolution.json](../experiments/results/autonomous_leaky_recovery_outer_high_resolution.json)
and its resolution and claim audit in
[leaky-outer-high-resolution-artifact.md](leaky-outer-high-resolution-artifact.md).
The previously committed binary64 scalar orbit diagnostics and monodromy
summaries remain in
[autonomous_leaky_recovery_bistable_probe.json](../experiments/results/autonomous_leaky_recovery_bistable_probe.json).
That record does not store replayable branch states or Fourier coefficients.
The separately tracked inner artifact stores the complete 129-node binary64
polynomial, phase reference, parameters, diagnostics and source hashes.  The
outer artifact stores an independent 129--385 node resolution ladder and uses
the 257-node polynomial for its directed proof.

## 1. The first incompatibility is an equation mismatch

The old periodic validator treats

\[
 w'=\varepsilon(v-a).
\tag{1.1}
\]

The autonomous bistable model instead has

\[
 w'=\varepsilon(v-a-w).
\tag{1.2}
\]

For normalized phase \(\theta=t/T\), its slow Fourier equation is

\[
 \mathcal F_{w,k}(v,w,T)
 =2\pi ikw_k-T\varepsilon(v_k-a\delta_{k0}-w_k).
\tag{1.3}
\]

Consequently, relative to the old validator,

\[
\begin{aligned}
 \mathcal F_w^{\rm leak}-\mathcal F_w^{\rm old}
   &=T\varepsilon w,\\
 D_w\mathcal F_w^{\rm leak}-D_w\mathcal F_w^{\rm old}
   &=T\varepsilon I,\\
 \partial_T\mathcal F_w^{\rm leak}
   -\partial_T\mathcal F_w^{\rm old}
   &=\varepsilon w.
\end{aligned}
\tag{1.4}
\]

These are exact identities.  They are not perturbative error terms.  Calling
the old validator on either leaky candidate would certify a different RFDE.
The tests evaluate the residual and period-column identities mode by mode,
check the changed recovery diagonal, and separately exercise the changed
majorants.  The independent proof of the complete adaptation is recorded in
[leaky-periodic-majorant-audit.md](leaky-periodic-majorant-audit.md).

The old parameter-box theorem also has the wrong coordinates: it encloses
\((\kappa _1,\kappa _3)\), whereas the biological response theorem requires
\((a,\kappa _3)\).  Its parameter sensitivities and box residual therefore
cannot be relabeled.

## 2. What is reusable

The following pieces do not depend on the recovery leak and are reused
without changing their mathematical meaning:

1. the real-conjugate Fourier coefficient space and its weighted independent
   real coordinates;
2. exact MPFR enclosures of Fourier delay rotations;
3. de-aliased cubic convolution and the finite/tail projections;
4. the stored binary64 midpoint inverse together with directed Higham
   matrix-product and matrix-vector error bounds;
5. the analytic inverse \((2\pi ik)^{-1}\) on tail modes; and
6. cancellation of the mode factor arising from differentiation of a moving
   delay by that tail inverse.

The engineering reuse is therefore about 75--85 percent for the center
periodic-BVP code.  This percentage is a code-architecture estimate, not a
mathematical statement.

The model-dependent changes are exactly the three slow-row expressions in
(1.4), the recovery tail-column majorant, the \((a,\kappa _3)\) parameter
forcing, and every orbit-dependent Floquet matrix.  In the component Wiener
norm, the lower-order recovery input column changes from \(1\) to

\[
 1+\varepsilon.
\tag{2.1}
\]

The validator includes this term in the tail-to-tail bound and enlarges the
correction-ball linear majorant by
\(\varepsilon\max\{\|A_P\|,\|D_Q^{-1}\|\}\).  It reuses none of the old
proof flags or stored Floquet artifacts.

## 3. Center finite/tail contract

For each branch \(\Gamma\in\{\Gamma_p,\Gamma_u\}\), let
\(\bar x=(\bar v,\bar w,\bar T)\) be a finite Fourier polynomial.  The proof
must be carried out in the same real-conjugate Wiener space as the old
validator, but for the leaky map (1.3).  With a cutoff \(M\) containing the
full cubic support, form

\[
 J_{PP}^{\rm leak}=WRP D\mathcal F^{\rm leak}(\bar x)PEW^{-1}
\tag{3.1}
\]

and precondition the complement by \((2\pi ik)^{-1}\).  Acceptance for one
center orbit requires directed bounds

\[
 Y=\|A\mathcal F^{\rm leak}(\bar x)\|,
 \qquad
 Z_0=\|I-A D\mathcal F^{\rm leak}(\bar x)\|<1,
\tag{3.2}
\]

together with a correction-ball bound

\[
 \|A(D\mathcal F^{\rm leak}(\bar x+h)
        -D\mathcal F^{\rm leak}(\bar x))\|
 \le Z_1r+Z_2r^2+Z_3r^3.
\tag{3.3}
\]

For some declared \(r>0\), the radii inequality is

\[
 Y+\{Z_0+Z_1r+Z_2r^2+Z_3r^3\}r<r,
 \qquad
 Z_0+Z_1r+Z_2r^2+Z_3r^3<1.
\tag{3.4}
\]

The new source evaluates every endpoint in (3.2)--(3.4) with the existing
directed backend.  On the source-hashed inner artifact, cutoff 192 and
160-bit arithmetic give

\[
 Z_{\rm full}<0.031543,\qquad q<0.091563,
 \qquad r-P(r)>9.08\times10^{-6}
 \quad (r=10^{-5}).
\]

Together with the independent derivation of every changed term, these strict
inequalities validate a unique phase-fixed inner RFDE orbit in the declared
Wiener ball and validate its phase-bordered derivative.  They do not determine
any Floquet multiplier count.

The original 65-node outer-branch smoke calculation exposed a resolution
blocker:

\[
 Y\approx4.49\times10^{-4},\qquad Z_0\approx0.3242,
 \qquad Z_1\approx1.43\times10^4.
\tag{3.5}
\]

At that resolution no radius can simultaneously dominate \(Y\) and keep the
linear contraction term small.  A fresh 129--385 node continuation ladder
shows that the off-grid defect falls from \(3.51\times10^{-5}\) at 129 nodes
to \(8.13\times10^{-12}\) at 257 nodes.  For the 257-node polynomial, cutoff
384 and 160-bit arithmetic give

\[
 Y<2.571\times10^{-13},\qquad
 Z_{\rm full}<0.081215,\qquad q(10^{-5})<0.242071,
\]

and a positive radii margin greater than \(7.579\times10^{-6}\).  These bounds
validate a distinct phase-fixed outer RFDE orbit and its phase-bordered
inverse.  They do not prove that the outer orbit is attracting.

## 4. Parameter-box contract

With both center orbits proved, the next continuation gate is one common rectangle

\[
 U=\{|a-\tfrac14|\le r_a,
       |\kappa _3-\tfrac1{200}|\le r_3\},
\tag{4.1}
\]

with \(\varepsilon=1/5\), \(\kappa _1=1/250\), and the two delays fixed.
The exact parameter columns are

\[
 \partial_a\mathcal F=(0,T\varepsilon),
\tag{4.2}
\]

and

\[
 \partial_{\kappa _3}\mathcal F
 =\left(-T\varepsilon\left\{
 \frac{S_0(v-1)^3+S_1(v-1)^3}{2}-(v-1)^3
 \right\},0\right).
\tag{4.3}
\]

Acceptance requires two uniform radii inequalities, disjoint orbit tubes,
and directed isolation of one voltage maximum and one minimum on each
branch.  The common box is needed for the later response and onset theorem;
two unrelated center certificates do not supply it.

## 5. Floquet contract

The old Floquet results are tied to the old orbit, gains, slow equation,
coefficient matrices, and artifact hashes.  Only their abstract strategy is
reusable.  Roughly 30--40 percent of the implementation architecture carries
over; no spectral conclusion does.

For each validated leaky branch, the required sequence is:

1. Use time-translation invariance to identify the tangent solution.  A
   phase-bordered inverse can then control the geometric periodic kernel,
   conditional on the standard periodic-BVP identification.
2. Prove the Fredholm-to-history-monodromy multiplicity transfer.  Without
   it, a bordered BVP inverse does not prove algebraic simplicity of the
   multiplier one.
3. Construct a directed resolvent/Bloch cover of the unit circle away from
   one.
4. Deflate the neutral direction and compute a directed Riesz trace or
   determinant winding on the exterior annulus.  Pointwise invertibility of
   contour matrices alone does not determine the integer.
5. Certify

   \[
    \nu(\Gamma_p)=0,
    \qquad
    \nu(\Gamma_u)=1,
   \tag{5.1}
   \]

   where \(\nu\) is the algebraic count of nontranslation multipliers outside
   the unit disk.

The binary64 spectra provide favorable margins: the leading outer
nontranslation multiplier is approximately \(-0.02195\), and the inner
branch has one real multiplier approximately \(2.01045\) while its next
reported multipliers are of order \(10^{-6}\).  These values motivate the
contours but do not certify (5.1).

## 6. Claim ledger and recommended order

**Exact now:** the identities (1.3)--(1.4), the changed Fourier Jacobian
layout, the finite/tail and nonlinear majorant adaptation, and the parameter
columns (4.2)--(4.3).

**Directed proof:** MPFR endpoint evaluation of the leaky finite/tail radii
quantities validates distinct source-bound inner and outer periodic orbits
and their phase-bordered derivatives.

**Floating-point evidence:** the finite monodromy spectra and their suggested
zero/one nontranslation unstable-index split.

**Open:** the common parameter box, algebraic simplicity of the neutral
multipliers, unit-circle exclusion, the two unstable-index counts, directed
extrema, and all stable-manifold and pulse-routing conclusions.

The efficient order is now: build the common \((a,\kappa _3)\) orbit and
extrema box; perform the two unit-circle covers and Riesz counts; construct
the inner stable covector/manifold; and validate the pulse intersection and
two-sided routing.  The finite-section separator candidate can choose the
center of that last proof, but cannot replace it.
