# Stage 3F: combined advanced rows for the signed outer kernel

## 1. Why this replaces separate H/L bounds

Stage 3E proves a strict multiplicative transfer for \(F\) and \(G\), but
separate uniform estimates of \(H_j\) and \(L_{jk}\) give errors of order
\(190\) and \(7.2\times10^6\).  Those estimates destroy exactly the
cancellation that makes the return operator small.  They are not used here.

For a voltage output at \(t=T+\sigma\), define the single combined row

\[
 p_\sigma(u)=e_v^TR(T+\sigma,u)1_{u\le T+\sigma}
 -\frac{q_v(\sigma)}{q_v(0)}e_v^TR(T,u).
\]

For the recovery output, set

\[
 p_w(u)=\left(e_w^T-\frac{q_w(0)}{q_v(0)}e_v^T\right)R(T,u).
\]

Away from the terminal jumps, either row satisfies the advanced equation

\[
 -p'(u)=p(u)A(u)+\sum_j p(u+\tau_j)B_j(u+\tau_j).
\]

The phase-corrected history density and recovery atom are then

\[
 k(\theta)=\sum_{j:\theta\ge-\tau_j}
 p(\theta+\tau_j)B_j(\theta+\tau_j)e_v,
 \qquad c=p(0)e_w.
\]

All delay words, both injection branches and phase subtraction are therefore
inside \(p\) before an absolute value is taken.  This is the central
compression of Stage 3F.

## 2. Strictly closed pieces

The Stage-3E 1024-cell, degree-24 polynomial charts are replayed with
160-bit outward MPFR arithmetic.  On every cell the adjugate polynomial is
integrated and divided by the proved determinant lower bound.  Combining
this with the exact F/G multiplicative errors gives two rigorous quantities:

- an instantaneous normalized-phase Green integral bound;
- an instantaneous boundary-propagator bound.

The certificate also includes the exact \(10^{-8}\) orbit and period ball,
both delayed-coefficient variations including the delay-phase shift, and
strict voltage/recovery phase-ratio transfer errors.  These are proof
objects, not binary diagnostics.

## 3. Direct center diagnostic and residual targets

A source-bound binary64 pilot evaluates the full DDE resolvent and the two
combined rows directly.  It never constructs an absolute H/L budget.  The
pilot records the full-DDE Green scale, the two combined-row sizes, and the
continuous-density center norms.  These values remain diagnostic.

The JSON then writes the exact closing inequality in budget form.  It
reserves \(10^{-2}\) for center total-variation transfer and asks for a full
advanced Green bound below \(60000\), a boundary bound below \(70000\), and
the displayed row-residual thresholds.  It also subtracts the already proved
instantaneous Green and boundary pieces, exposing the precise allowance left
for delayed feedback.

The voltage budget is the tight one.  The orbit and delayed-coefficient
defects are rank one, so they multiply the voltage component of \(p\), not
the full row norm; only the period-matrix defect pays the full row.  This
preserved structure materially enlarges the delayed-Green allowance.  The
binary center full-DDE Green is orders of magnitude smaller than the resulting
ceiling, so there is no observed numerical obstruction.

## 4. Remaining claim boundary

The delayed part of the advanced Green/boundary estimates and a
degree-24, 192-bit tensor Bernstein residual for the two combined rows have
not yet been emitted.  Hence the displayed residual budgets are sufficient
targets, not achieved error bounds.  \(E_v\) and \(E_w\) remain null;
arbitrary-\(C^0\) contraction, nonlinear attraction, capture and physical
onset all remain false.
