# Wide physical-pulse family at the inner Route-C section

Status: **directed prefix plus one complete rational shard; executable
family contract, not a wide-family, event, separator, onset, or routing
theorem.**

The target pulse interval is the exact rational interval

\[
 I_J=[6021/20000,753/2500]=[0.30105,0.30120].
\]

Route C is source-bound to

\[
 h_C(\phi)=\phi_v(0)-V_{\rm true}(0),
\]

where the parent validates the phase-zero inner-orbit voltage and a positive
orbit-section speed on its declared radius-
\(10^{-2}\) ball.  Those are orbit-section constants.  They do not prove
that any physical pulse reaches that ball or crosses this exact section.

## What the present directed calculation proves

The degree-24 method of steps uses 192-bit outward MPFR arithmetic on the
same exact two-origin \(\mathbb Q(\sqrt5)\) grid as the quiet-pulse proof.
Both delay translations, \(4\sqrt5\) and \(5\sqrt5\), and the release at
time one are retained exactly.

An unsplit symmetric tube for all of \(I_J\) closes 730 of the requested
1152 cells.  It first loses a finite endpoint bound on the cell

\[
 [365\sqrt5/24,\;1+355\sqrt5/24],
\]

leaving exactly 422 time cells.  The last closed prefix already has maximum
\(P\)-radius about \(49.8864\).  This is a rigorous failure of this
particular enclosure, not evidence that the RFDE family diverges.

For an executable fallback, partition \(I_J\) into 30,000 exact equal
subintervals of width \(1/200000000\), with centers

\[
 c_k=6021/20000+(2k+1)/400000000,
 \qquad k=0,\ldots,29999.
\]

The registered pilot is partition member \(k=15000\), centered at
\(120450001/400000000\), with half-width \(1/400000000\).  All 1152 cells
close.  Its maximum state \(P\)-radius is less than \(9.678\times10^{-3}\),
and its minimum cell-closure gap is greater than
\(6.22\times10^{-13}\).  This leaves 29,999 partition members unreplayed.
The numerical cap \(10^{-2}\) here is a **P-norm pilot cap**, not the Route-C
history-ball radius: norm conversion, guide-to-orbit distance, event-time
error, and a continuous complete-history comparison are still required.

## Why 30,000 shards are not the real breakthrough

State sharding is computationally executable.  It is not the main
mathematical obstruction.  On the accepted shard, the zero-centered scalar
majorants for the first and second \(J\)-variations reach approximately

\[
 3.844\times10^6,\qquad 2.546\times10^{13}.
\]

At zero parameter width they still reach approximately
\(3.817\times10^6\) and \(2.510\times10^{13}\).  Thus shrinking shards does
not remove the long-time wrapping in those variation coordinates.  Even a
full 30,000-shard state replay would not supply a useful event derivative or
stable-coordinate monotonicity bound.

The replacement proof coordinate should be a cellwise parameter Taylor
model

\[
 z(t,J)=z_0(t)+\delta z_1(t)+\frac{\delta^2}{2}z_2(t)
       +\frac{\delta^3}{6}z_3(t)+\frac{\delta^4}{24}z_4(t)+R_5(t,\delta),
\]

with the coefficient guides propagated together and only the highest-order
remainder enclosed symmetrically.  The event must then be solved as an
implicit jet \(\tau(J)\), and the whole history
\(\theta\mapsto z(\tau(J)+\theta,J)\) must be pulled back to the common
event graph.  This retains the correlations discarded by the present
zero-centered norm majorants.

## Stable-coordinate interface

The future separator coordinate is

\[
 H(J)=\ell_u(y_u(J))-h_s(y_s(J)),
\]

using a validated RFDE unstable Riesz covector \(\ell_u\) and a validated
local stable graph \(h_s\).  Both endpoint values and the uniform derivative
of this exact \(H\) are currently null.  The observed finite-section numbers
\(+1.1780\times10^{-3}\) and \(-9.0826\times10^{-4}\) are preserved only as
diagnostics.  A finite left vector is not the RFDE covector, so these signs
are not evidence for either side of the stable manifold.

Consequently the unique Route-C pulse event and speed, event-time first and
second variations, common-event complete-history tube, endpoint stable
signs, stable-gap monotonicity, onset threshold, and two-sided basin routing
all remain false.

Reproduce the registered artifact with

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 \
  experiments/leaky_pulse_inner_route_c_family_contract.py
```

Use `--check` for the source/hash audit and `--check --recompute` for the
three expensive directed replays.
