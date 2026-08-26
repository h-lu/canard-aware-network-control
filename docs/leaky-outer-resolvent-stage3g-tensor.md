# Stage 3G: directed tensor residual for the complete outer resolvent

> **AUDIT NOTICE (2026-08-26).** The v1 artifact is retracted: it covered only 20 of the
> 40 terminal-clipped cells because it used `final_lag_cell=46-delta_cell`
> although \(T/h=47.5914\ldots\). All v1 complete-cover, Green/bootstrap,
> and downstream size claims are withdrawn. The text below describes the
> corrected 730+40-cell v2 construction; only a matching source-bound v2
> result and its independent replays may support the corrected claims.

## 1. Moving-frame equation

Put

\[
 S(\delta,\ell)=R(T-\delta,T-\delta-\ell),
 \qquad 0\leq\delta\leq\tau_1,
 \quad 0\leq\ell\leq T-\delta .
\]

Then

\[
 \partial_\ell S
 =SA(T-\delta-\ell)
 +\sum_j S(\delta,\ell-\tau_j)
 B_j(T-\delta-\ell+\tau_j).
\]

The mesh width is \(h=\tau_1/20\).  In binary64 arithmetic
\(\tau_0=16h\) and \(\tau_1=20h\) exactly, so every delayed chart has the
same local tensor coordinates as the current chart.  This is the finite
method-of-steps compression used by the proof.

## 2. Complete geometry, including the terminal cells

There are 730 rectangles wholly below
\(\delta+\ell=T\), plus 40 cells cut by that terminal line.  Indeed
\(T/h=47.5914\ldots\), so the terminal line crosses two lag cells in each
delta column.  This is now a directed geometry gate, not a floating-point
observation: the certificate records outward bounds proving
\(47h<T<48h\), \(0<49h-T<0.85\), and that the last quantity is below the
terminal continuation solve horizon.  A zero-cost preflight derives and
checks 730 ordinary cells, 40 clipped cells, and 12,320 local tensor
patches before any expensive residual sweep.  During replay these fields,
including the guide-period hex value, are recomputed from the pinned
257-node outer parent rather than trusted as mutually consistent JSON
claims.  Directly
interpolating the old finite-word formula over a cut cell is invalid: its
nonphysical side has the wrong derivative at the initial-time boundary.
For candidate construction only, Stage 3G continues the matrix row through
that side by the same retarded equation for less than (0.8) physical time
units.  The
full extended rectangle is then revalidated by the directed residual.
Consequently its physical clipped subset is covered without a Duffy
remainder or an unproved triangular sliver.

## 3. Directed tensor arithmetic

Each matrix component has a degree-10 Chebyshev coordinate in \(\delta\)
and degree 24 in \(\ell\).  Candidate coefficients are stored binary64
numbers and treated as exact dyadics.  Exact rational change-of-basis maps
send the candidate to local tensor Bernstein form.  Current and delayed
coefficients use cutoff-128 Fourier--Taylor models of degree 24.  Their
retained coefficients, Taylor remainders, and omitted Fourier tails are
enclosed outward.

All change of basis, degree elevation, tensor products, signed residual
sums, and final row norms use 192-bit Arb balls.  No residual component is
normed before the current and both delayed contributions have been added.
Initial-boundary and one-sided lag-interface defects are separate atoms.

The four closing thresholds are never converted through binary64.  The
Green and boundary targets are exact integers in Arb, while the voltage
and recovery residual targets are ingressed character-for-character from
the two Stage-3F row contracts and compared with lower endpoints of their
exact-decimal Arb enclosures.  The latter parent rows, including exponent
format, are part of the replay contract.

Stage 3G also validates the complete Stage-3D parent source manifest before
constructing `_PrimitiveGuide`; this locks the phase-fixed-return,
continuous-kernel, delay-word, interval, orbit, and model sources used by
that guide.  The already loaded Stage-3D parent is passed explicitly into
the tensor builder, so repository selection cannot silently fall back to a
path derived from `__file__`.

## 4. Green bootstrap and claim boundary

The candidate uniform and normalized-integral bounds, together with the
matrix residual and chart atoms, give a target bootstrap for the exact
advanced Green integral and boundary propagator.  The JSON records the
strict result and compares it with the Stage-3F targets 60000 and 70000.

The numerical refinement ledger formerly printed here belonged to the
incomplete v1 cover and is therefore withdrawn, even though its maximizer
was reported in an ordinary cell.  The corrected source-bound v2 JSON is
the sole numerical ledger: it records the polynomial, Fourier-tail,
interface, Green, and phase-ratio contributions after both terminal cells
in every delta column have been included.  No v1 residual or bootstrap
number is evidence for a v2 gate.

The same JSON records that both joint augmented \(S/U\) residual targets
strictly pass.  This consequence is rigorous but uses a uniform phase-ratio
triangle bound.  It is not substituted for a tight direct bound on the two
phase-combined row sizes.  Until those strict sizes replace the Stage-3F
binary diagnostics, \(E_v\), \(E_w\), arbitrary \(C^0\) contraction,
nonlinear attraction, capture, and physical onset all remain open.

The validator checks exact top-level and nested schemas, identity and
parent maps, environment and source locks, flag uniqueness/disjointness,
and numerical/Boolean agreement of all four strict gates before performing
the expensive independent replay.  Hostile tests refresh the certificate
digest after mutating claims, parents, geometry, or gate values, ensuring
that rejection is semantic rather than merely a stale-digest side effect.
The coefficient Taylor cache is also fixed at
\(48\cdot3\cdot(2\cdot4-1)=1008\) entries.  The conclusion is an exact
source constant; a refreshed-digest attempt to append an onset claim is
rejected before replay.
