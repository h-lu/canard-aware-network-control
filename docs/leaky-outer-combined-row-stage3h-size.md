# Stage 3H: output-specific strict sizes for the combined outer rows

> **AUDIT NOTICE (2026-08-26).** The v1 sizes are retracted because they consumed the incomplete
> Stage-3G 730+20-cell cover and therefore omitted the second terminal cell
> in each delta column. Its strict-size flags and numerical bounds are
> withdrawn. Only a matching source-bound v2 result against the corrected
> Stage-3G 730+40-cell v2 certificate may support the sizes below.

## 1. The row that is enclosed

For \(t=T-\delta\), \(u=t-\ell\), Stage 3H encloses the voltage row

\[
 p_v(\delta,\ell)=e_v^T S(\delta,\ell)
 -\alpha(\delta)e_v^T S(0,\delta+\ell),
 \qquad \alpha(\delta)=q_v(-\delta)/q_v(0),
\]

as one signed object.  The recovery row

\[
 p_w(\ell)=e_w^T S(0,\ell)-\beta e_v^T S(0,\ell),
 \qquad \beta=q_w(0)/q_v(0),
\]

is treated in the same way.  No bound on \(S\) and no uniform phase-ratio
multiple is substituted before these subtractions.

Here the phase-ratio centers come from the frozen binary center orbit, while
\(S\) is the exact guide resolvent certified from the Stage-3G candidate.
Thus these are *center-guide* row sizes.  The exact-orbit phase and
coefficient transfer remains in the separately displayed frontier costs; it
is not silently absorbed into the row-size claim.

On each local patch the binary phase-ratio center is treated as an exact
dyadic.  A cutoff-128, degree-24 Fourier--Taylor/Bernstein enclosure gives
the strict radius around it.  The center is combined with both components of
the terminal row before a row norm is taken; only then is the radius cost
added.

## 2. Event seams and the terminal line

In a current chart, the terminal argument is

\[
 (\delta+\ell)/h=i+j+1+(x+y)/2.
\]

Thus \(x+y=0\) is a lag-chart seam.  Stage 3H never interpolates through
that seam.  It constructs the lower and upper terminal-chart polynomials
separately.  Each polynomial is bounded on the full local square, which is a
rigorous superset of its physical triangular half.  This is conservative but
retains the one-sided event chart.  Since \(T/h=47.5914\ldots\), two clipped
lag cells are retained in every delta column.  Only the nominal upper side
of the second clipped cell lies beyond the physical domain and is not used.

The terminal row \(S(0,\delta+\ell)\) is composed algebraically: the
degree-10 delta coordinate is evaluated at its exact endpoint, the remaining
degree-24 Chebyshev polynomial is composed with
\(z=z_c+(X+Y)/4\), and exact rational power-to-Bernstein maps are applied in
both coordinates.  Candidate coefficients are exact dyadics and all matrix
arithmetic uses 192-bit Arb balls.

## 3. Transfer from the Stage-3G candidate

The Stage-3G Green bootstrap proves a uniform row error between the
piecewise candidate and the exact guide resolvent.  Stage 3H first bounds the
direct signed candidate row, then adds

\[
 (1+|\alpha|)\,\|S-\widehat S\|
 \quad\hbox{or}\quad
 (1+|\beta|)\,\|S-\widehat S\|.
\]

Consequently the reported center-guide full-row and voltage-component sizes
are strict;
the Stage-3F binary size pilot is no longer used as a proof input.  Their
outward decimal values and maximizer cells are stated only in the matching
source-bound v2 JSON, so the withdrawn v1 values cannot be mistaken for the
corrected cover.  The validator checks the maximizer's chart side, event
flag, clipped-cell flag, and patch coordinates before performing the full
replay.

## 4. Exact claim boundary

This stage deliberately stops one step before \(E_v,E_w\).  The strict
sizes, Stage-3G residual/Green theorem, and Stage-3F exact-orbit defect
budgets make the final contraction inequality conditional only on validating
the reserved \(10^{-2}\) transfer between the Stage-2 discrete signed shadow
and a directed continuous center-density cell integral.  That integral must
still sum both delayed injection branches inside each phase-corrected row
before absolute value.  Until it is emitted, \(E_v,E_w\), arbitrary-
\(C^0\) contraction, nonlinear attraction, capture, and onset remain false.

For orientation only, the certificate records the two conditional totals
obtained after adding the full reserved \(0.01\).  The validator requires both
totals to be below one and verifies their nonnegative component ledger.  They
remain a frontier, not \(E_v,E_w\): the reserve itself is the remaining
theorem.

The v2 result is bound to the final Stage-3G-v2 result digest
`52d2c4df0cea7b6d98d898669e45ef54bfed1799965b2cff92161e84bd78ce13`
and validates every source hash in the Stage-3G parent manifest before using
its candidate or Green error.
