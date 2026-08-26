# Outer signed matrix-measure kernel: Stage 2

Status: **directed discrete signed-kernel pilot and continuous cell contract;
not yet a (C^0)-history operator bound.**  This stage explains and audits
the large phase cancellation seen in Stage 1, distinguishes the exact Dirac,
density, and scalar parts of the RFDE solution operator, and reduces the
one-return linear theorem to two continuous transfer errors.  It proves no
outer attraction, capture, routing, or pulse onset.

The executable source is
[the Stage-2 module](../src/canard_control/leaky_outer_signed_kernel_stage2.py),
the generator is
[the experiment](../experiments/leaky_outer_signed_kernel_stage2.py), and the
tracked output is
[the result](../experiments/results/leaky_outer_signed_kernel_stage2.json).

## 1. The exact measure decomposition

Along the exact outer orbit, write the linear RFDE as

\[
 x'(t)=A(t)x(t)+\sum_{j=0}^1B_j(t)x(t-\tau_j),
\]

where each (B_j) has only its fast-row/current-voltage entry nonzero.  Let
(R(t,s)) be its causal principal resolvent:

\[
 R(t,s)=0\quad(t<s),\qquad R(s,s)=I,
\]

\[
 \partial_tR(t,s)=A(t)R(t,s)
 +\sum_jB_j(t)R(t-\tau_j,s).
\]

For reduced initial history (h=(h_v,h_w(0))), the solution has three
different input objects:

\[
 x(t)=R(t,0)e_vh_v(0)
      +\int_{-\tau_1}^0K(t,\theta)h_v(\theta)\,d\theta
      +R(t,0)e_wh_w(0),
\]

with

\[
 K(t,\theta)=
 \sum_{j:\,-\tau_j\leq\theta\leq0}
 R(t,\theta+\tau_j)B_j(\theta+\tau_j)e_v.
\]

Thus the first term is a current-value Dirac atom, the second is an
absolutely continuous history density, and the third is an independent
scalar column.  Since tangent directions on the physical phase section
satisfy (h_v(0)=0), the sole Dirac atom is killed exactly.  It must not be
mixed into a quadrature density or paid as a generic history error.

## 2. Phase subtraction before total variation

For (-\tau_1\leq\sigma\leq0), the returned voltage-history kernel is

\[
 K_c(T+\sigma,\theta)=K(T+\sigma,\theta)
 -\frac{q(T+\sigma)}{q_v(T)}K_v(T,\theta),
\]

and the same subtraction is made in the scalar (h_w(0)) column.  The
recovery output uses the recovery component at (sigma=0).  Only after this
signed subtraction may one bound

\[
 \int_{-\tau_1}^0|K_{c,i}(t,\theta)|\,d\theta
 +|c_{c,i}(t)|.
\]

This ordering is essential.  On the physical output rows of the 360-step
pilot, the fixed-time shadow and the rank-one phase shadow separately have
infinity norm about (2.585).  Their triangle bound is above (5.16).
Directed subtraction coefficient by
coefficient gives a norm below (0.127).  A proof that separately estimates
the two terms cannot see the neutral-direction cancellation and cannot
close.

## 3. What is directed in this artifact

The stored binary64 Fourier tangent (q=\dot X_o) is used instead of a
computed unit eigenvector.  The 360-step RK4/cubic-interpolation monodromy is
the exact stored binary matrix for this pilot.  For every physical returned
row (i) and every retained input column (j), the artifact encloses

\[
 M_{ij}-q_iM_{hj}/q_h
\]

with 160-bit outward MPFR operations.  It then takes interval absolute values
and sums them with upward rounding.  Each output row records separately:

- fixed-time history mass and recovery scalar;
- rank-one phase history mass and recovery scalar;
- corrected history mass and recovery scalar;
- the contribution from four interpolation-padding cells;
- sign-definite and zero-containing coefficient counts; and
- a digest of all directed corrected cell intervals.

The physical history begins at matrix index four.  The four earlier values
exist only because cubic interpolation needs padding; their largest corrected
mass is about (1.12\times10^{-8}).  They are exposed rather than silently
identified with physical history.

The directed shadow bounds are approximately

\[
 Q_{v,h}<0.127,\qquad Q_{w,h}<0.00277,
\]

and hence leave more than (0.873) below one.  The discrete phase-chart
shadow norm is about (1.93903).  These statements are rigorous only for the
exact stored binary matrix and its exact stored Fourier tangent.  RK4
truncation, cubic interpolation, the exact-orbit radius, and the continuum of
input histories are not hidden inside the MPFR rounding intervals.

## 4. The remaining continuous cell proof

A closing certificate must propagate (R(t,s)), (K(t,\theta)), the scalar
column, and the tangent over

\[
 0\leq s\leq\tau_1,qquad T-\tau_1\leq t\leq T,
 \qquad -\tau_1\leq\theta\leq0
\]

by interval Taylor, Bernstein, or an equivalent directed Volterra method of
steps.  It must include the nested (10^{-8}) exact-orbit/period ball.  Each
\(\theta\)-cell must enclose the signed phase-corrected density before
integrating its absolute value.  Sampling the input history is forbidden:
the total-variation bound itself is what covers every (h_v\in C^0).

Let (E_v,E_w) bound the difference between the exact continuous row norms
and the registered shadow bounds.  The sole first-order numerical gate is

\[
 \boxed{
 \max\{Q_{v,h}+E_v,Q_{w,h}+E_w\}<1 .
 }
\]

There is room for transfer error of roughly (0.873), so the pilot gives no
numerical obstruction.  The registered (E_v,E_w) fields remain null because
the continuous density cells have not yet been emitted.  Consequently the
arbitrary-(C^0) operator bound and linear return contraction remain false.

For ambient pulse attachment, a third transfer error (E_{\rm phase}) turns
the discrete phase-chart shadow into a continuous (Q_{\rm phase}).  The
separate Stage-1 gate
(Q_{\rm phase}d_X<r_{\rm section}) is still required; a voltage event does
not place a pulse history on the exact phase section.
